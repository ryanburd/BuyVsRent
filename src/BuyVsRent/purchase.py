import numpy as np
import pandas as pd

import incomeAndTax as iat


class purchase:

    def __init__(
        self,
        purchase_price: int,
        down_payment_percent: float,
        interest_APR_yearly: float,
        hoa_monthly: float,
        loan_length_years: int = 30,
        hoa_percent_increase_yearly: float = 3,
        tax_percent_yearly: float = 1,
        tax_percent_increase_yearly: float = 1,
        insurance_monthly: int = 150,
        insurance_percent_increase_yearly: float = 5,
        pmi_percent_yearly: float = 1,
        maintenance_percent_yearly: float = 1,
        buying_costs_percent: float = 4,
        selling_costs_percent: float = 6,
        appreciation_percent_yearly: float = 2,
        investment_gains_percent_yearly: float = 8,
    ):

        # --- Values used by other class functions ---
        self.appreciation_percent_yearly = appreciation_percent_yearly
        self.tax_percent_increase_yearly = tax_percent_increase_yearly
        self.insurance_percent_increase_yearly = insurance_percent_increase_yearly
        self.hoa_percent_increase_yearly = hoa_percent_increase_yearly
        self.pmi_percent_yearly = pmi_percent_yearly
        self.maintenance_percent_yearly = maintenance_percent_yearly
        self.investment_gains_percent_yearly = investment_gains_percent_yearly

        # --- Values calculated from the user-provided details ---
        loan_length_months: int = loan_length_years * 12
        self.down_payment: float = purchase_price * down_payment_percent / 100
        self.initial_loan_balance: float = purchase_price - self.down_payment
        self.no_pmi_balance: float = purchase_price * 0.8
        self.interest_rate_monthly: float = interest_APR_yearly / 100 / 12
        self.pi_monthly: float = (
            self.initial_loan_balance
            * self.interest_rate_monthly
            * (1 + self.interest_rate_monthly) ** (loan_length_months)
            / ((1 + self.interest_rate_monthly) ** (loan_length_months) - 1)
        )
        self.buying_costs = purchase_price * buying_costs_percent / 100

        # --- DataFrame that stores values for different metrics each month of the loan ---
        self.df = pd.DataFrame(
            0.0,
            index=range(1, loan_length_months + 1),
            columns=[
                "Home value",
                "Equity",
                "Loan balance",
                "Principal",
                "Interest",
                "Tax home value",
                "Real estate tax %",
                "Real estate taxes",
                "Home insurance",
                "PITI",
                "HOA",
                "PMI",
                "Total housing payment (28%)",
                "Maintenance",
                "Total with maintenance",
                "State tax",
                "Itemizable expenses",
                "Federal tax",
                "Total with main. & tax",
                "Investment balance",
                "Investment gains",
                "Investment deposited",
                "Total assets",
            ],
        )

        # Initialize each metric
        self.df.loc[1, "Home value"] = purchase_price
        self.df.loc[1, "Equity"] = self.down_payment
        self.df.loc[1, "Loan balance"] = self.initial_loan_balance
        self.df.loc[1, "Interest"] = (
            self.initial_loan_balance * self.interest_rate_monthly
        )
        self.df.loc[1, "Principal"] = self.pi_monthly - self.df.loc[1, "Interest"]
        self.df.loc[1, "Tax home value"] = purchase_price
        self.df.loc[1, "Real estate tax %"] = tax_percent_yearly
        self.df.loc[1, "Real estate taxes"] = (
            purchase_price * tax_percent_yearly / 100 / 12
        )
        self.df.loc[1, "Home insurance"] = insurance_monthly
        self.df.loc[1, "HOA"] = hoa_monthly
        self.df.loc[1, "PMI"] = (
            self.initial_loan_balance * pmi_percent_yearly / 100 / 12
        )

    def update_home_value(self, month):
        self.df.loc[month, "Home value"] = self.df.loc[month - 1, "Home value"] * (
            (1 + self.appreciation_percent_yearly / 100) ** (1 / 12)
        )

    def update_equity(self, month):
        self.df.loc[month, "Equity"] = (
            self.df.loc[month - 1, "Equity"]
            + self.df.loc[month - 1, "Principal"]
            + (self.df.loc[month, "Home value"] - self.df.loc[month - 1, "Home value"])
        )

    def update_loan_balance(self, month):
        self.df.loc[month, "Loan balance"] = (
            self.df.loc[month - 1, "Loan balance"] - self.df.loc[month - 1, "Principal"]
        )
        if abs(self.df.loc[month, "Loan balance"]) < 1:
            self.df.loc[month, "Loan balance"] = 0

    def update_interest(self, month):
        self.df.loc[month, "Interest"] = (
            self.df.loc[month, "Loan balance"] * self.interest_rate_monthly
        )

    def update_principal(self, month):
        if self.df.loc[month, "Loan balance"] == 0:
            self.df.loc[month, "Principal"] = 0
        else:
            self.df.loc[month, "Principal"] = (
                self.pi_monthly - self.df.loc[month, "Interest"]
            )

    def update_real_estate_taxes(self, month):
        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "Tax home value"] = self.df.loc[
                month - 1, "Tax home value"
            ]
        else:
            self.df.loc[month, "Tax home value"] = self.df.loc[
                month - 1, "Tax home value"
            ] * (1 + self.appreciation_percent_yearly / 100)

        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "Real estate tax %"] = self.df.loc[
                month - 1, "Real estate tax %"
            ]
        else:
            self.df.loc[month, "Real estate tax %"] = self.df.loc[
                month - 1, "Real estate tax %"
            ] * (1 + self.tax_percent_increase_yearly / 100)

        self.df.loc[month, "Real estate taxes"] = (
            self.df.loc[month, "Tax home value"]
            * self.df.loc[month, "Real estate tax %"]
            / 100
            / 12
        )

    def update_insurance(self, month):
        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "Home insurance"] = self.df.loc[
                month - 1, "Home insurance"
            ]
        else:
            self.df.loc[month, "Home insurance"] = self.df.loc[
                month - 1, "Home insurance"
            ] * (1 + self.insurance_percent_increase_yearly / 100)

    def update_hoa(self, month):
        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "HOA"] = self.df.loc[month - 1, "HOA"]
        else:
            self.df.loc[month, "HOA"] = self.df.loc[month - 1, "HOA"] * (
                1 + self.hoa_percent_increase_yearly / 100
            )

    def update_pmi(self, month):
        if self.df.loc[month, "Loan balance"] > self.no_pmi_balance:
            self.df.loc[month, "PMI"] = (
                self.initial_loan_balance * self.pmi_percent_yearly / 100 / 12
            )

    def calculate_piti(self):
        self.df["PITI"] = (
            self.df["Principal"]
            + self.df["Interest"]
            + self.df["Real estate taxes"]
            + self.df["Home insurance"]
        )

    def calculate_total_housing_payment(self):
        self.df["Total housing payment (28%)"] = (
            self.df["PITI"] + self.df["HOA"] + self.df["PMI"]
        )

    def calculate_maintenance_costs(self):
        self.df["Maintenance"] = (
            self.df["Home value"] * self.maintenance_percent_yearly / 100 / 12
        )

    def calculate_total_with_main(self):
        self.df["Total with maintenance"] = (
            self.df["Total housing payment (28%)"] + self.df["Maintenance"]
        )

    def calculate_state_tax(self, iat):
        self.df["State tax"] = iat.df["Yearly state standard taxes"] / 12

    def calculate_item_expenses(self):
        self.df["Itemizable expenses"] = (
            self.df["Interest"] + self.df["Real estate taxes"] + self.df["State tax"]
        )

    def calculate_federal_tax(self, iat):
        self.df["Federal tax"] = (
            iat.df[
                ["Yearly federal standard taxes", "Yearly federal itemized taxes"]
            ].min(axis=1)
            / 12
        )

    def calculate_total_with_tax(self):
        self.df["Total with main. & tax"] = (
            self.df["Total with maintenance"] + self.df["Federal tax"]
        )

    def initialize_deposited(self, renter):
        if (
            self.df.loc[1, "Total with main. & tax"]
            < renter.df.loc[1, "Total with tax"]
        ):
            self.df.loc[1, "Investment deposited"] = (
                renter.df.loc[1, "Total with tax"]
                - self.df.loc[1, "Total with main. & tax"]
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

    def update_deposited(self, month, renter):
        if (
            self.df.loc[month, "Total with maintenance"]
            < renter.df.loc[month, "Total housing payment (28%)"]
        ):
            self.df.loc[month, "Investment deposited"] = (
                renter.df.loc[month, "Total housing payment (28%)"]
                - self.df.loc[month, "Total with maintenance"]
            )
        else:
            self.df.loc[month, "Investment deposited"] = 0

    def calculate_total_assets(self):
        self.df["Total assets"] = self.df["Equity"] + self.df["Investment balance"]


if __name__ == "__main__":
    example_purchase = purchase(
        purchase_price=650_000,
        down_payment_percent=10,
        interest_APR_yearly=7.125,
        hoa_monthly=425,
        years_in_house=30.1,
        loan_length_years=30,
        hoa_percent_increase_yearly=3,
        tax_percent_yearly=1.053,
        tax_percent_increase_yearly=1,
        insurance_monthly=150,
        insurance_percent_increase_yearly=5,
        pmi_percent_yearly=0.2,
        maintenance_percent_yearly=1,
        buying_costs_percent=4,
        selling_costs_percent=6,
        appreciation_percent_yearly=2,
    )

    print(example_purchase.df)
