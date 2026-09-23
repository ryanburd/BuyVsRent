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
    ):

        # --- Values used by other class functions ---
        self.rent_percent_increase_yearly: float = rent_percent_increase_yearly
        self.hoa_percent_increase_yearly: float = hoa_percent_increase_yearly
        self.insurance_percent_increase_yearly: float = (
            insurance_percent_increase_yearly
        )
        self.investment_gains_percent_yearly = investment_gains_percent_yearly

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
