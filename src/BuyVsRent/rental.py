import numpy as np
import pandas as pd


class rental:

    def __init__(
        self,
        rent_monthly: float,
        hoa_monthly: float,
        insurance_yearly: float,
        rent_percent_increase_yearly: float = 3,
        hoa_percent_increase_yearly: float = 3,
        insurance_percent_increase_yearly: float = 5,
        investment_gains_percent_yearly: float = 8,
        loan_length_years: float = 30,
        capital_gains_tax_percent: float = 15,
    ):

        # --- Values used by other class functions ---
        self.rent_percent_increase_yearly: float = rent_percent_increase_yearly
        self.hoa_percent_increase_yearly: float = hoa_percent_increase_yearly
        self.insurance_percent_increase_yearly: float = (
            insurance_percent_increase_yearly
        )
        self.investment_gains_percent_yearly = investment_gains_percent_yearly
        self.capital_gains_tax_percent = capital_gains_tax_percent

        # --- Values calculated from user-provided details ---
        insurance_monthly: float = insurance_yearly / 12
        loan_length_months: float = np.round(loan_length_years * 12, 0)

        # --- Initializing the dataframe to store all time-based metrics for the rental. The main script will update the dataframe. ---
        self.df = pd.DataFrame(
            0.0,
            index=range(1, loan_length_months + 1),
            columns=[
                "Rent",
                "HOA",
                "Rent insurance",
                "Total housing payment (28%)",
                "Federal tax",
                "Total with tax",
                "Investment balance",
                "Investment gains",
                "Investment deposited",
                "Cumulative investment sale tax",
                "Net assets",
            ],
        )

        # --- Initialize the first month of expenses ---
        self.df.loc[1, "Rent"] = rent_monthly
        self.df.loc[1, "HOA"] = hoa_monthly
        self.df.loc[1, "Rent insurance"] = insurance_monthly

    def update_rent(self, month):
        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "Rent"] = self.df.loc[month - 1, "Rent"]
        else:
            self.df.loc[month, "Rent"] = self.df.loc[month - 1, "Rent"] * (
                1 + self.rent_percent_increase_yearly / 100
            )

    def update_hoa(self, month):
        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "HOA"] = self.df.loc[month - 1, "HOA"]
        else:
            self.df.loc[month, "HOA"] = self.df.loc[month - 1, "HOA"] * (
                1 + self.hoa_percent_increase_yearly / 100
            )

    def update_insurance(self, month):
        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "Rent insurance"] = self.df.loc[
                month - 1, "Rent insurance"
            ]
        else:
            self.df.loc[month, "Rent insurance"] = self.df.loc[
                month - 1, "Rent insurance"
            ] * (1 + self.insurance_percent_increase_yearly / 100)

    def calculate_total_payment(self):
        self.df["Total housing payment (28%)"] = (
            self.df["Rent"] + self.df["HOA"] + self.df["Rent insurance"]
        )

    def calculate_federal_taxes(self, iat):
        self.df["Federal tax"] = iat.df["Yearly federal standard taxes"] / 12

    def calculate_total_with_tax(self):
        self.df["Total with tax"] = (
            self.df["Total housing payment (28%)"] + self.df["Federal tax"]
        )

    def initialize_balance(self, buyer):
        self.df.loc[1, "Investment balance"] = buyer.down_payment + buyer.buying_costs

    def intialize_gains(self):
        self.df.loc[1, "Investment gains"] = self.df.loc[1, "Investment balance"] * (
            (1 + self.investment_gains_percent_yearly / 100) ** (1 / 12) - 1
        )

    def initialize_deposited(self, buyer):
        if buyer.df.loc[1, "Total with main. & tax"] > self.df.loc[1, "Total with tax"]:
            self.df.loc[1, "Investment deposited"] = (
                buyer.df.loc[1, "Total with main. & tax"]
                - self.df.loc[1, "Total with tax"]
            )
        else:
            self.df.loc[1, "Investment deposited"] = 0

    def initialize_investment_tax(self, iat):
        gross_income = min(
            iat.df.loc[1, "Federal standard gross income"],
            iat.df.loc[1, "Federal itemized gross income"],
        )
        if gross_income < iat.federal_tax_brackets["10 % max"]:
            marginal_tax_percent = 10
        elif gross_income < iat.federal_tax_brackets["12 % max"]:
            marginal_tax_percent = 12
        elif gross_income < iat.federal_tax_brackets["22 % max"]:
            marginal_tax_percent = 22
        elif gross_income < iat.federal_tax_brackets["24 % max"]:
            marginal_tax_percent = 24
        elif gross_income < iat.federal_tax_brackets["32 % max"]:
            marginal_tax_percent = 32
        elif gross_income < iat.federal_tax_brackets["35 % max"]:
            marginal_tax_percent = 35
        else:
            marginal_tax_percent = 37
        self.df.loc[1, "Cumulative investment sale tax"] = (
            self.df.loc[1, "Investment gains"] * marginal_tax_percent / 100
        )

    def update_balance(self, month):
        self.df.loc[month, "Investment balance"] = (
            self.df.loc[month - 1, "Investment balance"]
            + self.df.loc[month - 1, "Investment gains"]
            + self.df.loc[month - 1, "Investment deposited"]
        )

    def update_gains(self, month):
        self.df.loc[month, "Investment gains"] = self.df.loc[
            month, "Investment balance"
        ] * ((1 + self.investment_gains_percent_yearly / 100) ** (1 / 12) - 1)

    def update_deposited(self, month, buyer):
        if (
            buyer.df.loc[month, "Total with maintenance"]
            > self.df.loc[month, "Total housing payment (28%)"]
        ):
            self.df.loc[month, "Investment deposited"] = (
                buyer.df.loc[month, "Total with maintenance"]
                - self.df.loc[month, "Total housing payment (28%)"]
            )
        else:
            self.df.loc[month, "Investment deposited"] = 0

    def update_cumulative_investment_tax(self, month, iat, savings):
        if savings:
            first_month_marginal = 1
        else:
            first_month_marginal = max(month - 11, 1)
        gross_income = iat.df.loc[month, "Federal standard gross income"]
        if gross_income < iat.federal_tax_brackets["10 % max"]:
            marginal_tax_percent = 10
        elif gross_income < iat.federal_tax_brackets["12 % max"]:
            marginal_tax_percent = 12
        elif gross_income < iat.federal_tax_brackets["22 % max"]:
            marginal_tax_percent = 22
        elif gross_income < iat.federal_tax_brackets["24 % max"]:
            marginal_tax_percent = 24
        elif gross_income < iat.federal_tax_brackets["32 % max"]:
            marginal_tax_percent = 32
        elif gross_income < iat.federal_tax_brackets["35 % max"]:
            marginal_tax_percent = 35
        else:
            marginal_tax_percent = 37
        self.df.loc[month, "Cumulative investment sale tax"] = (
            self.df.loc[: first_month_marginal - 1, "Investment gains"].sum()
            * self.capital_gains_tax_percent
            / 100
            + self.df.loc[first_month_marginal:month, "Investment gains"].sum()
            * marginal_tax_percent
            / 100
        )

    def calculate_net_assets(self):
        self.df["Net assets"] = (
            self.df["Investment balance"] - self.df["Cumulative investment sale tax"]
        )
