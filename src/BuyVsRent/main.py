import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from buyer import buyer
from renter import renter

if __name__ == "__main__":

    investment_gains_percent_yearly = 8

    buyer_1 = buyer(
        purchase_price=650_000,
        down_payment_percent=5,
        interest_APR_yearly=6.5,
        hoa_monthly=425,
        tax_percent_yearly=1.053,
        insurance_monthly=150,
        insurance_percent_increase_yearly=5,
        pmi_percent_yearly=0.5,
        maintenance_percent_yearly=1,
        buying_costs_percent=4,
        selling_costs_percent=6,
        appreciation_percent_yearly=2,
        investment_gains_percent_yearly=investment_gains_percent_yearly,
    )

    renter_1 = renter(
        rent_monthly=3_200,
        hoa_monthly=0,
        insurance_yearly=200,
        rent_percent_increase_yearly=3,
        insurance_percent_increase_yearly=5,
        investment_gains_percent_yearly=investment_gains_percent_yearly,
    )
