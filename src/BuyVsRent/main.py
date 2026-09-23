import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from purchase import purchase
from rental import rental
from incomeAndTax import incomeAndTax


def calculate_assets(
    buyer: purchase,
    renter: rental,
    iat: incomeAndTax,
    loan_length_years: float,
    years_in_home: float,
):

    # --- Loop through each month of the loan and update metrics for the renter, income, and standard taxes ---
    loan_length_months: int = np.round(loan_length_years * 12, 0)
    for m in range(2, loan_length_months + 1):

        buyer.update_home_value(month=m)
        buyer.update_equity(month=m)
        buyer.update_loan_balance(month=m)
        buyer.update_interest(month=m)
        buyer.update_principal(month=m)
        buyer.update_real_estate_taxes(month=m)
        buyer.update_insurance(month=m)
        buyer.update_hoa(month=m)
        buyer.update_pmi(month=m)

        renter.update_rent(month=m)
        renter.update_hoa(month=m)
        renter.update_insurance(month=m)

        iat.update_yearly_income(month=m)

        iat.update_yearly_federal_std_deduction(month=m)
        iat.update_yearly_federal_std_gross(month=m)
        iat.update_yearly_federal_brackets(month=m)
        iat.update_yearly_federal_std_taxes(month=m)

        iat.update_yearly_state_std_deduction(month=m)
        iat.update_yearly_state_std_gross(month=m)
        iat.update_yearly_state_brackets(month=m)
        iat.update_yearly_state_std_taxes(month=m)

    # --- Update the first month's YEARLY taxes with standard deduction. These values can't be initialized before the time-loop because _________ ---
    iat.update_first_month_taxes()

    # --- Calculate buyer's metrics that can be done outside the time-loop ---
    buyer.calculate_piti()
    buyer.calculate_total_housing_payment()
    buyer.calculate_maintenance_costs()
    buyer.calculate_total_with_main()
    buyer.calculate_state_tax(iat=iat)
    buyer.calculate_item_expenses()

    iat.calculate_yearly_federal_item_deduction(buyer=buyer)
    iat.calculate_yearly_federal_item_gross()
    iat.calculate_yearly_federal_item_taxes()

    buyer.calculate_federal_tax(iat=iat)
    buyer.calculate_total_with_tax()

    # --- Calculate renter's metrics that can be done outside the time-loop ---
    renter.calculate_total_payment()
    renter.calculate_federal_taxes(iat=iat)
    renter.calculate_total_with_tax()

    # --- Initialize investment metrics ---
    buyer.df.loc[1, "Investment balance"] = 0
    buyer.df.loc[1, "Investment gains"] = 0
    buyer.initialize_deposited(renter=renter)

    renter.initialize_balance(buyer=buyer)
    renter.intialize_gains()
    renter.initialize_deposited(buyer=buyer)

    # --- Loop through each month of the loan and calculate the buyer's and renter's investment metrics ---
    months_in_home: int = np.round(years_in_home * 12, 0)
    for m in range(2, months_in_home + 1):
        buyer.update_balance(month=m)
        buyer.update_gains(month=m)
        buyer.update_deposited(month=m, renter=renter)

        renter.update_balance(month=m)
        renter.update_gains(month=m)
        renter.update_deposited(month=m, buyer=buyer)

    # --- Calculate buyer's total assets ---
    buyer.calculate_total_assets()


def plot_assets(buyer: purchase, renter: rental, years_in_home: float):
    months_in_home = np.round(years_in_home * 12, 0)
    x_axis = buyer.df.index / 12
    plt.plot(x_axis, buyer.df["Total assets"], label="Buying")
    plt.plot(x_axis, renter.df["Investment balance"], label="Renting")
    plt.title("Total assets value of buying vs renting")
    plt.xlabel("Years")
    plt.xlim(0, years_in_home)
    plt.ylabel("Total assets value ($)")
    plt.ylim(
        0,
        1.1
        * max(
            buyer.df["Total assets"][months_in_home],
            renter.df["Investment balance"][months_in_home],
        ),
    )
    plt.legend()
    plt.show()


if __name__ == "__main__":

    # --- Values common to the purchase and rental for comparison ---
    loan_length_years = 30
    years_in_home = 10
    investment_gains_percent_yearly = 8

    # --- Initialize home purchases and home rentals
    purchase_1 = purchase(
        purchase_price=550_000,
        down_payment_percent=10,
        interest_APR_yearly=7.125,
        hoa_monthly=450,
        loan_length_years=loan_length_years,
        hoa_percent_increase_yearly=3,
        tax_percent_yearly=1.053,
        tax_percent_increase_yearly=1,
        insurance_monthly=80,
        insurance_percent_increase_yearly=3,
        pmi_percent_yearly=0.18,
        maintenance_percent_yearly=1,
        buying_costs_percent=3,
        selling_costs_percent=0,
        appreciation_percent_yearly=3,
        investment_gains_percent_yearly=8,
    )

    rental_1 = rental(
        rent_monthly=3_300,
        hoa_monthly=0,
        insurance_yearly=300,
        rent_percent_increase_yearly=3,
        hoa_percent_increase_yearly=3,
        insurance_percent_increase_yearly=3,
        investment_gains_percent_yearly=8,
        loan_length_years=loan_length_years,
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
        loan_length_years=loan_length_years,
    )

    # --- Create pairs of 1 home purchase and 1 home rental to compare the
    # buyer's and renter's asset values over time. Each pair must have a shared
    # defined investment gains % (yearly) ---

    calculate_assets(
        buyer=purchase_1,
        renter=rental_1,
        iat=iat_1,
        loan_length_years=loan_length_years,
        years_in_home=years_in_home,
    )

    plot_assets(buyer=purchase_1, renter=rental_1, years_in_home=years_in_home)
