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

        # --- Update the buyer and renter's investment gains % (yearly)
        self.buyer.investment_gains_percent_yearly = investment_gains_percent_yearly
        self.renter.investment_gains_percent_yearly = investment_gains_percent_yearly

        # --- Update the renter's investment balance array length to match the buyer's ---
        self.renter.investment_balance = np.zeros(self.buyer.loan_length_years * 12)

        # --- Update the initial asset values based on the home purchase price ---
        self.buyer.equity[0] = self.buyer.down_payment
        self.renter.investment_balance[0] = (
            self.buyer.down_payment + self.buyer.buying_costs
        )

        # --- Loop through each month and update monthly payments and asset value ---
        for m in range(self.buyer.loan_length_years * 12):
            buyer_interest = (
                self.buyer.initial_loan_balance * self.buyer.interest_rate_monthly
            )
            buyer_principal = self.buyer.pi_monthly - buyer_interest
            buyer_tax = self.buyer.home_value * self.buyer.tax_percent_yearly / 100 / 12
            buyer_insurance = self.buyer.insurance_monthly
            buyer_hoa = self.buyer.hoa_monthly
            buyer_pmi = (
                self.buyer.initial_loan_balance
                * self.buyer.pmi_percent_yearly
                / 100
                / 12
            )
            buyer_maintenance = (
                self.buyer.home_value * self.buyer.maintenance_percent_yearly / 100 / 12
            )
            self.buyer.current_month_payment = (
                buyer_principal
                + buyer_interest
                + buyer_tax
                + buyer_insurance
                + buyer_hoa
                + buyer_pmi
                + buyer_maintenance
            )

            renter_rent = self.renter.rent_monthly
            renter_hoa = self.renter.hoa_monthly
            renter_insurance = self.renter.insurance_monthly
            self.renter.current_month_payment = (
                renter_rent + renter_hoa + renter_insurance
            )


if __name__ == "__main__":

    # --- Define variables that will be used in other calculations ---
    loan_length_years = 30

    # --- Initialize home purchases and home rentals
    purchase_1 = purchase(
        purchase_price=650_000,
        down_payment_percent=5,
        interest_APR_yearly=6.5,
        hoa_monthly=425,
        loan_length_years=loan_length_years,
        hoa_percent_increase_yearly=3,
        tax_percent_yearly=1.053,
        tax_percent_increase_yearly=1,
        insurance_monthly=150,
        insurance_percent_increase_yearly=5,
        pmi_percent_yearly=0.5,
        maintenance_percent_yearly=1,
        buying_costs_percent=4,
        selling_costs_percent=6,
        appreciation_percent_yearly=2,
    )

    rental_1 = rental(
        rent_monthly=3_200,
        hoa_monthly=0,
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
