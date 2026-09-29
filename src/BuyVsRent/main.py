import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

from purchase import purchase
from rental import rental
from incomeAndTax import incomeAndTax


def calculate_assets(
    buyer: purchase,
    renter: rental,
    iat: incomeAndTax,
    loan_length_years: float,
    years_in_home: float,
    savings: bool,
):

    # --- Loop through each month of the loan and update metrics for the renter, income, and standard taxes ---
    months_in_home: int = np.round(years_in_home * 12, 0)
    loan_length_months: int = np.round(loan_length_years * 12, 0)
    for m in range(2, loan_length_months + 1):

        buyer.update_living_in(month=m)
        buyer.update_chargeable_rent(month=m)
        buyer.update_home_value(month=m)
        buyer.update_equity(month=m)
        buyer.update_loan_balance(month=m)
        buyer.update_interest(month=m)
        buyer.update_principal(month=m)
        buyer.update_family_pi(month=m)
        buyer.update_real_estate_taxes(month=m)
        buyer.update_insurance(month=m)
        buyer.update_hoa(month=m)
        buyer.update_pmi(month=m)

        renter.update_living_in(month=m)
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
    buyer.calculate_total_minus_rent()
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
    buyer.initialize_investment_tax(iat=iat)

    renter.initialize_balance(buyer=buyer)
    renter.intialize_gains()
    renter.initialize_deposited(buyer=buyer)
    renter.initialize_investment_tax(iat=iat)

    # --- Loop through each month of the loan and calculate the buyer's and renter's investment metrics ---
    for m in range(2, loan_length_months + 1):
        buyer.update_balance(month=m)
        buyer.update_gains(month=m)
        buyer.update_deposited(month=m, renter=renter)
        buyer.update_cumulative_investment_tax(month=m, iat=iat, savings=savings)

        renter.update_balance(month=m)
        renter.update_gains(month=m)
        renter.update_deposited(month=m, buyer=buyer)
        renter.update_cumulative_investment_tax(month=m, iat=iat, savings=savings)

    # --- Calculate buyer's total assets and cost to sell ---
    buyer.calculate_total_assets()
    buyer.calculate_selling_costs()
    buyer.calculate_cost_to_sell()
    buyer.calculate_net_assets()

    # --- Calculate renter's net assets---
    renter.calculate_net_assets()


def view_df(df):
    root = tk.Tk()
    root.withdraw()

    window = tk.Toplevel()
    window.title("DataFrame")

    # Include index as the first column
    columns = ["index"] + list(df.columns)

    # Create table
    tree = ttk.Treeview(window, columns=columns, show="headings")

    # Column headers
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Add rows, including index
    for index, row in df.iterrows():
        tree.insert("", "end", values=[index] + list(row))

    tree.pack(fill="both", expand=True)

    # Scrollbars
    scrollbar_y = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    scrollbar_y.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
    scrollbar_x.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=scrollbar_x.set)

    window.mainloop()


def plot_assets(
    short_buyer: purchase,
    short_renter: rental,
    long_buyer: purchase,
    long_renter: rental,
    years_in_home: float,
    loan_length_years: float,
):

    fig, axs = plt.subplots(2, 3, constrained_layout=True)

    months_in_home = np.round(years_in_home * 12, 0)
    short_x_axis = short_buyer.df[:months_in_home].index / 12
    long_x_axis = long_buyer.df.index / 12

    # --- Short-term scenarios ---
    axs[0, 0].plot(
        short_x_axis,
        short_buyer.df.loc[:months_in_home, "Total assets"],
        linestyle="-",
        color="tab:blue",
        label="Buying",
    )
    axs[0, 0].plot(
        short_x_axis,
        short_buyer.df.loc[:months_in_home, "Net assets"],
        linestyle="--",
        color="tab:blue",
        label="after selling",
    )
    axs[0, 0].plot(
        short_x_axis,
        short_renter.df.loc[:months_in_home, "Investment balance"],
        linestyle="-",
        color="tab:orange",
        label="Renting",
    )
    axs[0, 0].plot(
        short_x_axis,
        short_renter.df.loc[:months_in_home, "Net assets"],
        linestyle="--",
        color="tab:orange",
        label="after selling",
    )
    axs[0, 0].set_title("'Buy and Sell' vs 'Rent and Short-Term Save'")
    axs[0, 0].set_xlabel("Years")
    axs[0, 0].set_xlim(0, years_in_home)
    axs[0, 0].set_ylabel("Total assets value ($)")
    axs[0, 0].set_ylim(
        0,
        None,
    )
    axs[0, 0].legend()

    # --- Cost each month ---
    axs[0, 1].plot(
        short_x_axis,
        short_buyer.df.loc[:months_in_home, "Total minus rent"],
        linestyle="-",
        color="tab:blue",
        label="Buying",
    )
    axs[0, 1].plot(
        short_x_axis,
        short_buyer.df.loc[:months_in_home, "Total with tax"],
        linestyle="--",
        color="tab:blue",
        label="+ federal tax",
    )
    axs[0, 1].plot(
        short_x_axis,
        short_renter.df.loc[:months_in_home, "Total housing payment (28%)"],
        linestyle="-",
        color="tab:orange",
        label="Renting",
    )
    axs[0, 1].plot(
        short_x_axis,
        short_renter.df.loc[:months_in_home, "Total with tax"],
        linestyle="--",
        color="tab:orange",
        label="+ federal tax",
    )
    axs[0, 1].set_title("Monthly cost")
    axs[0, 1].set_xlabel("Years")
    axs[0, 1].set_xlim(0, years_in_home)
    axs[0, 1].set_ylabel("$")
    axs[0, 1].legend()

    # --- Money saved each month ---
    axs[0, 2].plot(
        short_x_axis,
        short_renter.df.loc[:months_in_home, "Investment deposited"],
        linestyle="-",
        color="tab:orange",
        label="Renting",
    )
    axs[0, 2].set_title("Money saved each month by renting")
    axs[0, 2].set_xlabel("Years")
    axs[0, 2].set_xlim(0, years_in_home)
    axs[0, 2].set_ylabel("$")
    axs[0, 2].set_ylim(
        0,
        None,
    )

    # --- Long-term scenarios ---
    axs[1, 0].plot(
        long_x_axis,
        long_buyer.df["Total assets"],
        linestyle="-",
        color="tab:blue",
        label="Buying",
    )
    axs[1, 0].plot(
        long_x_axis,
        long_buyer.df["Net assets"],
        linestyle="--",
        color="tab:blue",
        label="after selling",
    )
    axs[1, 0].plot(
        long_x_axis,
        long_renter.df["Investment balance"],
        linestyle="-",
        color="tab:orange",
        label="Renting",
    )
    axs[1, 0].plot(
        long_x_axis,
        long_renter.df["Net assets"],
        linestyle="--",
        color="tab:orange",
        label="after selling",
    )
    axs[1, 0].set_title("'Buy and Keep' vs 'Rent and Long-Term Save'")
    axs[1, 0].set_xlabel("Years")
    axs[1, 0].set_xlim(0, loan_length_years)
    axs[1, 0].set_ylabel("Total assets value ($)")
    axs[1, 0].set_ylim(
        0,
        None,
    )
    axs[1, 0].legend()

    # --- Cost each month ---
    axs[1, 1].plot(
        long_x_axis,
        long_buyer.df["Total minus rent"],
        linestyle="-",
        color="tab:blue",
        label="Buying",
    )
    # axs[1, 1].plot(
    #     long_x_axis,
    #     long_buyer.df["Total with tax"],
    #     linestyle="--",
    #     color="tab:blue",
    #     label="+ federal tax",
    # )
    axs[1, 1].plot(
        long_x_axis,
        long_renter.df["Total housing payment (28%)"],
        linestyle="-",
        color="tab:orange",
        label="Renting",
    )
    # axs[1, 1].plot(
    #     long_x_axis,
    #     long_renter.df["Total with tax"],
    #     linestyle="--",
    #     color="tab:orange",
    #     label="+ federal tax",
    # )
    axs[1, 1].set_title("Monthly cost")
    axs[1, 1].set_xlabel("Years")
    axs[1, 1].set_xlim(0, loan_length_years)
    axs[1, 1].set_ylabel("$")
    axs[1, 1].legend()

    # --- Money saved each month ---
    axs[1, 2].plot(
        long_x_axis,
        long_renter.df["Investment deposited"],
        linestyle="-",
        color="tab:orange",
        label="Renting",
    )
    axs[1, 2].set_title("Money saved each month by renting")
    axs[1, 2].set_xlabel("Years")
    axs[1, 2].set_xlim(0, loan_length_years)
    axs[1, 2].set_ylabel("$")
    axs[1, 2].set_ylim(
        0,
        None,
    )

    plt.show()


if __name__ == "__main__":

    # --- Define values common to all scenarios ---
    loan_length_years = 30
    years_in_home = 5
    capital_gains_tax_percent = 15

    # --- Define buying-specific metrics ---
    purchase_price = 550_000
    us_down_payment_percent = 15
    interest_rate_yearly = 7.125
    pmi_percent_yearly = 0.09  # 0.18 for 10%, 0.09 for 15%, 0 for 20%
    family_down_payment_percent = 0
    family_interest_rate_yearly = 1
    family_loan_length_years = 10
    hoa_monthly = 450
    chargeable_rent = 3_000  # HOW SHOULD THIS BE ESTIMATED? IT INFLUENCES THE PROSPECTS OF 'BUYING AND KEEPING' HEAVILY!
    rent_percent_increase_yearly = 3
    property_manager_cost_percent = 10
    hoa_percent_increase_yearly = 3
    tax_percent_yearly = 1.053
    tax_percent_increase_yearly = 1
    insurance_monthly = 150
    insurance_percent_increase_yearly = 3
    maintenance_percent_yearly = 0.25
    buying_costs_percent = 3
    selling_costs_percent = 7
    appreciation_percent_yearly = 2  # HOW SHOULD THIS BE ESTIMATED? IT INFLUENCES THE PROSPECTS OF BUYING HEAVILY!

    # --- Define renting-specific metrics ---
    rent_monthly = 2_900
    hoa_monthly = 0
    insurance_yearly = 456
    rent_percent_increase_yearly = 3
    hoa_percent_increase_yearly = 0
    insurance_percent_increase_yearly = 3

    # --- Create the "buy and sell" and short-term rent strategies ---
    short_investment_gains_percent_yearly = 3
    short_savings = True

    buy_and_sell = purchase(
        purchase_price=purchase_price,
        us_down_payment_percent=us_down_payment_percent,
        family_down_payment_percent=family_down_payment_percent,
        interest_rate_yearly=interest_rate_yearly,
        family_interest_rate_yearly=family_interest_rate_yearly,
        hoa_monthly=hoa_monthly,
        years_in_home=years_in_home,
        chargeable_rent=chargeable_rent,
        rent_percent_increase_yearly=rent_percent_increase_yearly,
        property_manager_percent_cost=property_manager_cost_percent,
        loan_length_years=loan_length_years,
        family_loan_length_years=family_loan_length_years,
        hoa_percent_increase_yearly=hoa_percent_increase_yearly,
        tax_percent_yearly=tax_percent_yearly,
        tax_percent_increase_yearly=tax_percent_increase_yearly,
        insurance_monthly=insurance_monthly,
        insurance_percent_increase_yearly=insurance_percent_increase_yearly,
        pmi_percent_yearly=pmi_percent_yearly,
        maintenance_percent_yearly=maintenance_percent_yearly,
        buying_costs_percent=buying_costs_percent,
        selling_costs_percent=selling_costs_percent,
        appreciation_percent_yearly=appreciation_percent_yearly,
        investment_gains_percent_yearly=short_investment_gains_percent_yearly,
        capital_gains_tax_percent=capital_gains_tax_percent,
    )

    rent_short = rental(
        rent_monthly=rent_monthly,
        hoa_monthly=hoa_monthly,
        insurance_yearly=insurance_yearly,
        years_in_home=years_in_home,
        rent_percent_increase_yearly=rent_percent_increase_yearly,
        hoa_percent_increase_yearly=hoa_percent_increase_yearly,
        insurance_percent_increase_yearly=insurance_percent_increase_yearly,
        investment_gains_percent_yearly=short_investment_gains_percent_yearly,
        loan_length_years=loan_length_years,
        capital_gains_tax_percent=capital_gains_tax_percent,
    )

    # --- Create the "buy and keep" and long-term rent strategies ---
    long_investment_gains_percent_yearly = 8  # HOW SHOULD THIS BE ESTIMATED? IT INFLUENCES THE PROSPECTS OF 'BUYING AND KEEPING' HEAVILY!
    long_savings = False

    buy_and_keep = purchase(
        purchase_price=purchase_price,
        us_down_payment_percent=us_down_payment_percent,
        family_down_payment_percent=family_down_payment_percent,
        interest_rate_yearly=interest_rate_yearly,
        family_interest_rate_yearly=family_interest_rate_yearly,
        hoa_monthly=hoa_monthly,
        years_in_home=years_in_home,
        chargeable_rent=chargeable_rent,
        rent_percent_increase_yearly=rent_percent_increase_yearly,
        property_manager_percent_cost=property_manager_cost_percent,
        loan_length_years=loan_length_years,
        family_loan_length_years=family_loan_length_years,
        hoa_percent_increase_yearly=hoa_percent_increase_yearly,
        tax_percent_yearly=tax_percent_yearly,
        tax_percent_increase_yearly=tax_percent_increase_yearly,
        insurance_monthly=insurance_monthly,
        insurance_percent_increase_yearly=insurance_percent_increase_yearly,
        pmi_percent_yearly=pmi_percent_yearly,
        maintenance_percent_yearly=maintenance_percent_yearly,
        buying_costs_percent=buying_costs_percent,
        selling_costs_percent=selling_costs_percent,
        appreciation_percent_yearly=appreciation_percent_yearly,
        investment_gains_percent_yearly=short_investment_gains_percent_yearly,
        capital_gains_tax_percent=capital_gains_tax_percent,
    )

    rent_long = rental(
        rent_monthly=rent_monthly,
        hoa_monthly=hoa_monthly,
        insurance_yearly=insurance_yearly,
        years_in_home=years_in_home,
        rent_percent_increase_yearly=rent_percent_increase_yearly,
        hoa_percent_increase_yearly=hoa_percent_increase_yearly,
        insurance_percent_increase_yearly=insurance_percent_increase_yearly,
        investment_gains_percent_yearly=long_investment_gains_percent_yearly,
        loan_length_years=loan_length_years,
        capital_gains_tax_percent=capital_gains_tax_percent,
    )

    # --- Define income and federal tax metrics ---
    iat = incomeAndTax(
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
        buyer=buy_and_sell,
        renter=rent_short,
        iat=iat,
        loan_length_years=loan_length_years,
        years_in_home=years_in_home,
        savings=short_savings,
    )

    calculate_assets(
        buyer=buy_and_keep,
        renter=rent_long,
        iat=iat,
        loan_length_years=loan_length_years,
        years_in_home=years_in_home,
        savings=long_savings,
    )

    print(
        f"\nOur all-in cost: ${purchase_price * us_down_payment_percent/100 + purchase_price * buying_costs_percent/100:,.0f}"
    )
    print(f"Us down payment: ${purchase_price * us_down_payment_percent/100:,.0f}")
    print(f"Buying costs: ${purchase_price * buying_costs_percent/100:,.0f}\n")
    print(
        f"Family down payment: ${purchase_price * family_down_payment_percent/100:,.0f}\n"
    )

    # view_df(buy_and_sell.df)

    plot_assets(
        short_buyer=buy_and_sell,
        short_renter=rent_short,
        long_buyer=buy_and_keep,
        long_renter=rent_long,
        years_in_home=years_in_home,
        loan_length_years=loan_length_years,
    )
