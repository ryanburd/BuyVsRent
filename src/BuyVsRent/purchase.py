import numpy as np
import pandas as pd


class purchase:

    def __init__(
        self,
        purchase_price: int,
        down_payment_percent: float,
        interest_APR_yearly: float,
        hoa_monthly: float,
        years_in_house: float,
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
    ):

        # --- User-provided details with no default value ---
        self.purchase_price: int = purchase_price
        self.initial_home_value: float = purchase_price
        self.down_payment_percent: float = down_payment_percent
        self.interest_APR_yearly: float = interest_APR_yearly
        self.hoa_monthly: float = hoa_monthly
        self.years_in_house: float = years_in_house

        # --- Details with default values. The user can override the defaul by providing a value ---
        self.loan_length_years: int = loan_length_years
        self.loan_length_months: int = self.loan_length_years * 12
        self.hoa_percent_increase_yearly: float = hoa_percent_increase_yearly
        self.tax_percent_yearly: float = tax_percent_yearly
        self.tax_percent_increase_yearly: float = tax_percent_increase_yearly
        self.insurance_monthly: int = insurance_monthly
        self.insurance_percent_increase_yearly: float = (
            insurance_percent_increase_yearly
        )
        self.pmi_percent_yearly: float = pmi_percent_yearly
        self.maintenance_percent_yearly: float = maintenance_percent_yearly
        self.buying_costs_percent: float = buying_costs_percent
        self.selling_costs_percent: float = selling_costs_percent
        self.appreciation_percent_yearly: float = appreciation_percent_yearly

        # --- Values calculated from the user-provided details ---
        self.months_in_house: int = int(np.round(self.years_in_house * 12, 0))
        self.down_payment: float = self.purchase_price * self.down_payment_percent / 100
        self.initial_loan_balance: float = self.purchase_price - self.down_payment
        self.current_loan_balance: float = self.initial_loan_balance
        self.no_pmi_balance: float = self.purchase_price * 0.8
        self.interest_rate_monthly: float = self.interest_APR_yearly / 100 / 12
        self.pi_monthly: float = (
            self.initial_loan_balance
            * self.interest_rate_monthly
            * (1 + self.interest_rate_monthly) ** (self.loan_length_months)
            / ((1 + self.interest_rate_monthly) ** (self.loan_length_months) - 1)
        )
        self.buying_costs = self.purchase_price * self.buying_costs_percent / 100

        # --- DataFrame that stores values for different metrics each month of the loan ---
        self.df_loan = pd.DataFrame(
            0.0,
            index=range(1, self.months_in_house + 1),
            columns=[
                "Home value",
                "Equity",
                "Loan balance",
                "Principal",
                "Interest",
                "Real estate tax %",
                "Real estate taxes",
                "Home insurance",
                "PITI",
                "HOA",
                "PMI",
                "Total housing payment (28%)",
                "Maintenance",
                "Total with maintenance",
                "Investment balance",
                "Investment gains",
                "Investment deposited",
                "Total assets",
            ],
        )

        # Initialize each metric
        self.df_loan.loc[1, "Home value"] = self.initial_home_value
        self.df_loan.loc[1, "Equity"] = self.down_payment
        self.df_loan.loc[1, "Loan balance"] = self.initial_loan_balance
        self.df_loan.loc[1, "Interest"] = (
            self.initial_loan_balance * self.interest_rate_monthly
        )
        self.df_loan.loc[1, "Principal"] = (
            self.pi_monthly - self.df_loan.loc[1, "Interest"]
        )
        self.df_loan.loc[1, "Real estate tax %"] = self.tax_percent_yearly
        self.df_loan.loc[1, "Real estate taxes"] = (
            self.initial_home_value * self.tax_percent_yearly / 100 / 12
        )
        self.df_loan.loc[1, "Home insurance"] = self.insurance_monthly
        self.df_loan.loc[1, "HOA"] = self.hoa_monthly
        self.df_loan.loc[1, "PMI"] = (
            self.initial_loan_balance * self.pmi_percent_yearly / 100 / 12
        )

        # --- Loop through each month of the loan and calculate metrics that need time-based calculations ---
        for m in range(2, self.months_in_house + 1):

            # Calculaute home value
            if np.mod(m - 1, 12) != 0:
                self.df_loan.loc[m, "Home value"] = self.df_loan.loc[
                    m - 1, "Home value"
                ]
            else:
                self.df_loan.loc[m, "Home value"] = self.df_loan.loc[
                    m - 1, "Home value"
                ] * (1 + self.appreciation_percent_yearly / 100)

            # Calculate equity
            self.df_loan.loc[m, "Equity"] = (
                self.df_loan.loc[m - 1, "Equity"]
                + self.df_loan.loc[m - 1, "Principal"]
                + (
                    self.df_loan.loc[m, "Home value"]
                    - self.df_loan.loc[m - 1, "Home value"]
                )
            )

            # Calculate loan balance
            self.df_loan.loc[m, "Loan balance"] = (
                self.df_loan.loc[m - 1, "Loan balance"]
                - self.df_loan.loc[m - 1, "Principal"]
            )
            if abs(self.df_loan.loc[m, "Loan balance"]) < 1:
                self.df_loan.loc[m, "Loan balance"] = 0

            # Calculate interest
            self.df_loan.loc[m, "Interest"] = (
                self.df_loan.loc[m, "Loan balance"] * self.interest_rate_monthly
            )

            # Calculate principal
            if self.df_loan.loc[m, "Loan balance"] == 0:
                self.df_loan.loc[m, "Principal"] = 0
            else:
                self.df_loan.loc[m, "Principal"] = (
                    self.pi_monthly - self.df_loan.loc[m, "Interest"]
                )

            # Calculate real estate taxes
            if np.mod(m - 1, 12) != 0:
                self.df_loan.loc[m, "Real estate tax %"] = self.df_loan.loc[
                    m - 1, "Real estate tax %"
                ]
            else:
                self.df_loan.loc[m, "Real estate tax %"] = self.df_loan.loc[
                    m - 1, "Real estate tax %"
                ] * (1 + self.tax_percent_increase_yearly / 100)

            self.df_loan.loc[m, "Real estate taxes"] = (
                self.df_loan.loc[m, "Home value"]
                * self.df_loan.loc[m, "Real estate tax %"]
                / 100
                / 12
            )

            # Calculate home insurance
            if np.mod(m - 1, 12) != 0:
                self.df_loan.loc[m, "Home insurance"] = self.df_loan.loc[
                    m - 1, "Home insurance"
                ]
            else:
                self.df_loan.loc[m, "Home insurance"] = self.df_loan.loc[
                    m - 1, "Home insurance"
                ] * (1 + self.insurance_percent_increase_yearly / 100)

            # Calculate HOA fee
            if np.mod(m - 1, 12) != 0:
                self.df_loan.loc[m, "HOA"] = self.df_loan.loc[m - 1, "HOA"]
            else:
                self.df_loan.loc[m, "HOA"] = self.df_loan.loc[m - 1, "HOA"] * (
                    1 + self.hoa_percent_increase_yearly / 100
                )

            # Calculate PMI
            if self.df_loan.loc[m, "Loan balance"] > self.no_pmi_balance:
                self.df_loan.loc[m, "PMI"] = (
                    self.initial_loan_balance * self.pmi_percent_yearly / 100 / 12
                )

        # --- Calculate columns that don't need time-based calculations ---

        # Calculate PITI
        self.df_loan["PITI"] = (
            self.df_loan["Principal"]
            + self.df_loan["Interest"]
            + self.df_loan["Real estate taxes"]
            + self.df_loan["Home insurance"]
        )

        # Calculate total housing payment, excluding maintenance. This is the 28% rule number.
        self.df_loan["Total housing payment (28%)"] = (
            self.df_loan["PITI"] + self.df_loan["HOA"] + self.df_loan["PMI"]
        )

        # Calculate average maintenance costs
        self.df_loan["Maintenance"] = (
            self.df_loan["Home value"] * self.maintenance_percent_yearly / 100 / 12
        )

        # Calculate total payment including maintenance
        self.df_loan["Total with maintenance"] = (
            self.df_loan["Total housing payment (28%)"] + self.df_loan["Maintenance"]
        )

        # --- Initializing investment related metrics. The main script will update these values. ---
        self.investment_gains_percent_yearly: float = 0


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

    print(example_purchase.df_loan)
