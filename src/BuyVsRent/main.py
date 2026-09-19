import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from purchase import purchase
from rental import rental
from income import income
from taxBrackets import taxBrackets


class buyerRenterComparison:

    def __init__(
        self,
        buyer: purchase,
        renter: rental,
        investment_gains_percent_yearly: float,
    ):

        # --- Define the buyer and renter
        self.buyer: purchase = buyer
        self.renter: rental = renter

        # --- Update values for the renter based on the buyer's data ---
        self.renter.years_in_house = self.buyer.years_in_house
        self.renter.months_in_house = self.buyer.months_in_house
        self.renter.initial_investment = (
            self.buyer.down_payment + self.buyer.buying_costs
        )

        # --- Initialize the renter's time-based dataframe metrics ---
        self.renter.df_rent.loc[1, "Rent"] = self.renter.rent_monthly
        self.renter.df_rent.loc[1, "HOA"] = self.renter.hoa_monthly
        self.renter.df_rent.loc[1, "Rent insurance"] = self.renter.insurance_monthly

        # --- Loop through each month of the loan and calculate the renter's metrics that need time-based calculations ---
        for m in range(2, self.renter.months_in_house + 1):

            # Calculate rent
            if np.mod(m - 1, 12) != 0:
                self.renter.df_rent.loc[m, "Rent"] = self.renter.df_rent.loc[
                    m - 1, "Rent"
                ]
            else:
                self.renter.df_rent.loc[m, "Rent"] = self.renter.df_rent.loc[
                    m - 1, "Rent"
                ] * (1 + self.renter.rent_percent_increase_yearly / 100)

            # Calculate HOA fee
            if np.mod(m - 1, 12) != 0:
                self.renter.df_rent.loc[m, "HOA"] = self.renter.df_rent.loc[
                    m - 1, "HOA"
                ]
            else:
                self.renter.df_rent.loc[m, "HOA"] = self.renter.df_rent.loc[
                    m - 1, "HOA"
                ] * (1 + self.renter.hoa_percent_increase_yearly / 100)

            # Calculate renter's insurance
            if np.mod(m - 1, 12) != 0:
                self.renter.df_rent.loc[m, "Rent insurance"] = self.renter.df_rent.loc[
                    m - 1, "Rent insurance"
                ]
            else:
                self.renter.df_rent.loc[m, "Rent insurance"] = self.renter.df_rent.loc[
                    m - 1, "Rent insurance"
                ] * (1 + self.renter.insurance_percent_increase_yearly / 100)

        # --- Calculate renter's metrics that are not time-based ---
        self.renter.df_rent["Total housing payment (28%)"] = (
            self.renter.df_rent["Rent"]
            + self.renter.df_rent["HOA"]
            + self.renter.df_rent["Rent insurance"]
        )

        # --- Update the buyer and renter's investment gains % (yearly)
        self.buyer.investment_gains_percent_yearly = investment_gains_percent_yearly
        self.renter.investment_gains_percent_yearly = investment_gains_percent_yearly

        # --- Initialize the buyer's investment metrics ---
        self.buyer.df_loan.loc[1, "Investment balance"] = 0
        self.buyer.df_loan.loc[1, "Investment gains"] = 0
        if (
            self.buyer.df_loan.loc[1, "Total with maintenance"]
            < self.renter.df_rent.loc[1, "Total housing payment (28%)"]
        ):
            self.buyer.df_loan.loc[1, "Investment deposited"] = (
                self.renter.df_rent.loc[1, "Total housing payment (28%)"]
                - self.buyer.df_loan.loc[1, "Total with maintenance"]
            )
        else:
            self.buyer.df_loan.loc[1, "Investment deposited"] = 0

        # --- Initialize the renter's investment metrics ---
        self.renter.df_rent.loc[1, "Investment balance"] = (
            self.renter.initial_investment
        )
        self.renter.df_rent.loc[1, "Investment gains"] = (
            self.renter.initial_investment
            * self.renter.investment_gains_percent_yearly
            / 100
            / 12
        )
        if (
            self.buyer.df_loan.loc[1, "Total with maintenance"]
            > self.renter.df_rent.loc[1, "Total housing payment (28%)"]
        ):
            self.renter.df_rent.loc[1, "Investment deposited"] = (
                self.buyer.df_loan.loc[1, "Total with maintenance"]
                - self.renter.df_rent.loc[1, "Total housing payment (28%)"]
            )
        else:
            self.renter.df_rent.loc[1, "Investment deposited"] = 0

        # --- Loop through each month of the loan and calculate the buyer's and renter's investment metrics ---
        for m in range(2, self.buyer.months_in_house + 1):
            # Calculate buyer's investment balance
            self.buyer.df_loan.loc[m, "Investment balance"] = (
                self.buyer.df_loan.loc[m - 1, "Investment balance"]
                + self.buyer.df_loan.loc[m - 1, "Investment gains"]
                + self.buyer.df_loan.loc[m - 1, "Investment deposited"]
            )

            # Calculate buyer's investment gains
            self.buyer.df_loan.loc[m, "Investment gains"] = (
                self.buyer.df_loan.loc[m, "Investment balance"]
                * self.buyer.investment_gains_percent_yearly
                / 100
                / 12
            )

            # Calculate buyer's investment deposit, if any
            if (
                self.buyer.df_loan.loc[m, "Total with maintenance"]
                < self.renter.df_rent.loc[m, "Total housing payment (28%)"]
            ):
                self.buyer.df_loan.loc[m, "Investment deposited"] = (
                    self.renter.df_rent.loc[m, "Total housing payment (28%)"]
                    - self.buyer.df_loan.loc[m, "Total with maintenance"]
                )
            else:
                self.buyer.df_loan.loc[m, "Investment deposited"] = 0

            # Calculate renter's investment balance
            self.renter.df_rent.loc[m, "Investment balance"] = (
                self.renter.df_rent.loc[m - 1, "Investment balance"]
                + self.renter.df_rent.loc[m - 1, "Investment gains"]
                + self.renter.df_rent.loc[m - 1, "Investment deposited"]
            )

            # Calculate renter's investment gains
            self.renter.df_rent.loc[m, "Investment gains"] = (
                self.renter.df_rent.loc[m, "Investment balance"]
                * self.renter.investment_gains_percent_yearly
                / 100
                / 12
            )

            # Calculate renter's investment deposit, if any
            if (
                self.buyer.df_loan.loc[m, "Total with maintenance"]
                > self.renter.df_rent.loc[m, "Total housing payment (28%)"]
            ):
                self.renter.df_rent.loc[m, "Investment deposited"] = (
                    self.buyer.df_loan.loc[m, "Total with maintenance"]
                    - self.renter.df_rent.loc[m, "Total housing payment (28%)"]
                )
            else:
                self.renter.df_rent.loc[m, "Investment deposited"] = 0

        # --- Calculate buyer's metrics that are not time-based ---
        self.buyer.df_loan["Total assets"] = (
            self.buyer.df_loan["Equity"] + self.buyer.df_loan["Investment balance"]
        )

        x_axis = self.buyer.df_loan.index / 12
        plt.plot(x_axis, self.buyer.df_loan["Total assets"], label="Buying")
        plt.plot(x_axis, self.renter.df_rent["Investment balance"], label="Renting")
        plt.title("Total assets value of buying vs renting")
        plt.xlabel("Years")
        plt.ylabel("Total assets value ($)")
        plt.legend()
        plt.show()


if __name__ == "__main__":

    # --- Initialize home purchases and home rentals
    purchase_1 = purchase(
        purchase_price=600_000,
        down_payment_percent=10,
        interest_APR_yearly=7.125,
        hoa_monthly=425,
        years_in_house=30,
        loan_length_years=30,
        hoa_percent_increase_yearly=3,
        tax_percent_yearly=1.053,
        tax_percent_increase_yearly=1,
        insurance_monthly=150,
        insurance_percent_increase_yearly=5,
        pmi_percent_yearly=0.2,
        maintenance_percent_yearly=1,
        buying_costs_percent=3,
        selling_costs_percent=6,
        appreciation_percent_yearly=3,
    )

    rental_1 = rental(
        rent_monthly=3_300,
        hoa_monthly=100,
        insurance_yearly=200,
        rent_percent_increase_yearly=3,
        hoa_percent_increase_yearly=3,
        insurance_percent_increase_yearly=5,
    )

    # --- Create pairs of 1 home purchase and 1 home rental to compare the
    # buyer's and renter's asset values over time. Each pair must have a shared
    # defined investment gains % (yearly) ---
    brc_1_investment_gains_percent_yearly = 8

    brc_1 = buyerRenterComparison(
        buyer=purchase_1,
        renter=rental_1,
        investment_gains_percent_yearly=brc_1_investment_gains_percent_yearly,
    )

    print(purchase_1.df_loan)
    print(rental_1.df_rent)

    # --- Define incomes ---
    income_1 = income(income_yearly=190_000, income_percent_increase_yearly=3)

    # --- Initialize current year tax brackets ---
    taxBrackets_1 = taxBrackets(
        standard_deduction=32_200,
        standard_deduction_percent_increase_yearly=3,
        bracket_maxes_married_jointly={
            0.1: 24_800,
            0.12: 100_800,
            0.22: 211_400,
            0.24: 403_550,
            0.32: 512_540,
            0.35: 768_700,
            0.37: None,
        },
        bracket_maxes_percent_increase_yearly=3,
    )
