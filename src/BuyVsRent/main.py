import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from purchase import purchase
from rental import rental
from incomeAndTax import incomeAndTax


class buyerRenterComparison:

    def __init__(
        self,
        buyer: purchase,
        renter: rental,
        iat: incomeAndTax,
        investment_gains_percent_yearly: float,
    ):

        # --- Define the buyer and renter
        self.buyer: purchase = buyer
        self.renter: rental = renter
        self.iat: incomeAndTax = iat

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

        # --- Create dataframe for YEARLY income and taxes each month ---
        self.df_iat = pd.DataFrame(
            0.0,
            index=range(1, self.buyer.months_in_house + 1),
            columns=[
                "Yearly income",
                "Federal standard deduction",
                "Federal standard gross income",
                "Yearly federal standard taxes",
                "Federal itemized deduction",
                "Federal itemized gross income",
                "Yearly federal itemized taxes",
                "10 % max",
                "12 % max",
                "22 % max",
                "24 % max",
                "32 % max",
                "35 % max",
                "37 % max",
                "State deduction",
                "State gross income",
                "Yearly state taxes",
                "2 % max",
                "3 % max",
                "5 % max",
                "5.75 % max",
            ],
        )

        # --- Initialize the first month of income and tax metrics ---
        self.df_iat.loc[1, "Yearly income"] = self.iat.income_yearly

        self.df_iat.loc[1, "Federal standard deduction"] = (
            self.iat.federal_standard_deduction
        )
        self.df_iat.loc[1, "Federal standard gross income"] = (
            self.iat.income_yearly - self.iat.federal_standard_deduction
        )
        self.df_iat.loc[1, "10 % max":"37 % max"] = self.iat.federal_tax_brackets

        self.df_iat.loc[1, "State deduction"] = self.iat.state_standard_deduction
        self.df_iat.loc[1, "State gross income"] = (
            self.iat.income_yearly - self.iat.state_standard_deduction
        )
        self.df_iat.loc[1, "2 % max":"5.75 % max"] = self.iat.state_tax_brackets

        # --- Loop through each month of the loan and calculate metrics ---
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

            # Calculate YEARLY income
            if np.mod(m - 1, 12) != 0:
                self.df_iat.loc[m, "Yearly income"] = self.df_iat.loc[
                    m - 1, "Yearly income"
                ]
            else:
                self.df_iat.loc[m, "Yearly income"] = self.df_iat.loc[
                    m - 1, "Yearly income"
                ] * (1 + self.iat.income_percent_increase_yearly / 100)

            # Calculate YEARLY federal standard deduction
            if np.mod(m - 1, 12) != 0:
                self.df_iat.loc[m, "Federal standard deduction"] = self.df_iat.loc[
                    m - 1, "Federal standard deduction"
                ]
            else:
                self.df_iat.loc[m, "Federal standard deduction"] = self.df_iat.loc[
                    m - 1, "Federal standard deduction"
                ] * (
                    1
                    + self.iat.federal_standard_deduction_percent_increase_yearly / 100
                )

            # Calculate YEARLY federal gross income with standard deduction
            self.df_iat.loc[m, "Federal standard gross income"] = (
                self.df_iat.loc[m, "Yearly income"]
                - self.df_iat.loc[m, "Federal standard deduction"]
            )

            # Calculate YEARLY federal tax bracket maximums
            if np.mod(m - 1, 12) != 0:
                self.df_iat.loc[m, "10 % max":"37 % max"] = self.df_iat.loc[
                    m - 1, "10 % max":"37 % max"
                ]
            else:
                self.df_iat.loc[m, "10 % max":"37 % max"] = self.df_iat.loc[
                    m - 1, "10 % max":"37 % max"
                ] * (1 + self.iat.federal_maxes_percent_increase_yearly / 100)

            # Calculate YEARLY federal taxes with standard deduction
            self.df_iat.loc[m, "Yearly federal standard taxes"] = (
                self.iat.calculate_federal_tax(
                    self.df_iat.loc[m, "Federal standard gross income"]
                )
            )

            # Calculate YEARLY state standard deduction
            if np.mod(m - 1, 12) != 0:
                self.df_iat.loc[m, "State deduction"] = self.df_iat.loc[
                    m - 1, "State deduction"
                ]
            else:
                self.df_iat.loc[m, "State deduction"] = self.df_iat.loc[
                    m - 1, "State deduction"
                ] * (
                    1 + self.iat.state_standard_deduction_percent_increase_yearly / 100
                )

            # Calculate YEARLY state gross income with standard deduction
            self.df_iat.loc[m, "State gross income"] = (
                self.df_iat.loc[m, "Yearly income"]
                - self.df_iat.loc[m, "State deduction"]
            )

            # Calculate YEARLY state tax bracket maximums
            if np.mod(m - 1, 12) != 0:
                self.df_iat.loc[m, "2 % max":"5.75 % max"] = self.df_iat.loc[
                    m - 1, "2 % max":"5.75 % max"
                ]
            else:
                self.df_iat.loc[m, "2 % max":"5.75 % max"] = self.df_iat.loc[
                    m - 1, "2 % max":"5.75 % max"
                ] * (1 + self.iat.state_maxes_percent_increase_yearly / 100)

            # Calculate YEARLY state taxes with standard deduction
            self.df_iat.loc[m, "Yearly state taxes"] = self.iat.calculate_state_tax(
                self.df_iat.loc[m, "State gross income"]
            )

        # --- Update the first month's YEARLY taxes with standard deduction (same as second month for quick calculation) ---
        self.df_iat.loc[1, "Yearly federal standard taxes"] = self.df_iat.loc[
            2, "Yearly federal standard taxes"
        ]

        self.df_iat.loc[1, "Yearly state taxes"] = self.df_iat.loc[
            2, "Yearly state taxes"
        ]

        # --- Calculate buyer's metrics that are not time-based ---
        self.buyer.df_loan["State tax"] = self.df_iat["Yearly state taxes"] / 12

        self.buyer.df_loan["Itemizable expenses"] = (
            self.buyer.df_loan["Interest"]
            + self.buyer.df_loan["Real estate taxes"]
            + self.buyer.df_loan["State tax"]
        )

        self.df_iat["Federal itemized deduction"] = (
            self.buyer.df_loan["Itemizable expenses"]
            .groupby(np.arange(len(self.buyer.df_loan)) // 12)
            .transform("sum")
        )

        self.df_iat["Federal itemized gross income"] = (
            self.df_iat["Yearly income"] - self.df_iat["Federal itemized deduction"]
        )

        self.df_iat["Yearly federal itemized taxes"] = self.df_iat[
            "Federal itemized gross income"
        ].apply(self.iat.calculate_federal_tax)

        self.buyer.df_loan["Federal tax"] = (
            self.df_iat[
                ["Yearly federal standard taxes", "Yearly federal itemized taxes"]
            ].min(axis=1)
            / 12
        )

        self.buyer.df_loan["Total with main. & tax"] = (
            self.buyer.df_loan["Total with maintenance"]
            + self.buyer.df_loan["Federal tax"]
        )

        # --- Calculate renter's metrics that are not time-based ---
        self.renter.df_rent["Total housing payment (28%)"] = (
            self.renter.df_rent["Rent"]
            + self.renter.df_rent["HOA"]
            + self.renter.df_rent["Rent insurance"]
        )

        self.renter.df_rent["Federal tax"] = (
            self.df_iat["Yearly federal standard taxes"] / 12
        )

        self.renter.df_rent["Total with tax"] = (
            self.renter.df_rent["Total housing payment (28%)"]
            + self.renter.df_rent["Federal tax"]
        )

        # --- Update the buyer and renter's investment gains % (yearly)
        self.buyer.investment_gains_percent_yearly = investment_gains_percent_yearly
        self.renter.investment_gains_percent_yearly = investment_gains_percent_yearly

        # --- Initialize the buyer's investment metrics ---
        self.buyer.df_loan.loc[1, "Investment balance"] = 0
        self.buyer.df_loan.loc[1, "Investment gains"] = 0
        if (
            self.buyer.df_loan.loc[1, "Total with main. & tax"]
            < self.renter.df_rent.loc[1, "Total with tax"]
        ):
            self.buyer.df_loan.loc[1, "Investment deposited"] = (
                self.renter.df_rent.loc[1, "Total with tax"]
                - self.buyer.df_loan.loc[1, "Total with main. & tax"]
            )
        else:
            self.buyer.df_loan.loc[1, "Investment deposited"] = 0

        # --- Initialize the renter's investment metrics ---
        self.renter.df_rent.loc[1, "Investment balance"] = (
            self.renter.initial_investment
        )
        self.renter.df_rent.loc[1, "Investment gains"] = (
            self.renter.initial_investment
            * ((1 + self.renter.investment_gains_percent_yearly / 100) ** (1 / 12) - 1)
        )
        if (
            self.buyer.df_loan.loc[1, "Total with main. & tax"]
            > self.renter.df_rent.loc[1, "Total with tax"]
        ):
            self.renter.df_rent.loc[1, "Investment deposited"] = (
                self.buyer.df_loan.loc[1, "Total with main. & tax"]
                - self.renter.df_rent.loc[1, "Total with tax"]
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
            self.buyer.df_loan.loc[m, "Investment gains"] = self.buyer.df_loan.loc[
                m, "Investment balance"
            ] * ((1 + self.buyer.investment_gains_percent_yearly / 100) ** (1 / 12) - 1)

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
            self.renter.df_rent.loc[m, "Investment gains"] = self.renter.df_rent.loc[
                m, "Investment balance"
            ] * (
                (1 + self.renter.investment_gains_percent_yearly / 100) ** (1 / 12) - 1
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

    def plot_assets(self):
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

    # --- Define income and federal tax metrics ---
    iat_1 = incomeAndTax(
        income_yearly=190_000,
        income_percent_increase_yearly=3,
        federal_standard_deduction=32_200,
        federal_standard_deduction_percent_increase_yearly=3,
        federal_tax_brackets={
            "10 % max": 24_800,
            "12 % max": 100_800,
            "22 % max": 211_400,
            "24 % max": 403_550,
            "32 % max": 512_540,
            "35 % max": 768_700,
            "37 % max": None,
        },
        federal_maxes_percent_increase_yearly=3,
        state_standard_deduction=17_500,
        state_standard_deduction_percent_increase_yearly=3,
        state_tax_brackets={
            "2 % max": 3_000,
            "3 % max": 5_000,
            "5 % max": 17_000,
            "5.75 % max": None,
        },
        state_maxes_percent_increase_yearly=3,
    )

    # --- Create pairs of 1 home purchase and 1 home rental to compare the
    # buyer's and renter's asset values over time. Each pair must have a shared
    # defined investment gains % (yearly) ---
    brc_1_investment_gains_percent_yearly = 8

    brc_1 = buyerRenterComparison(
        buyer=purchase_1,
        renter=rental_1,
        iat=iat_1,
        investment_gains_percent_yearly=brc_1_investment_gains_percent_yearly,
    )

    # print(purchase_1.df_loan.loc[:, "Total with main. & tax"].head(13))
    # print(rental_1.df_rent.loc[:, "Total with tax"].head(13))
    # print(brc_1.df_iat.head(13))
    brc_1.plot_assets()
