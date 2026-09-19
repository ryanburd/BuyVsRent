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
    ):

        # --- User-provided details with no default value ---
        self.rent_monthly: float = rent_monthly
        self.hoa_monthly: float = hoa_monthly
        self.insurance_yearly: float = insurance_yearly

        # --- Details with a default value. The user can override the default by providing a value ---
        self.rent_percent_increase_yearly: float = rent_percent_increase_yearly
        self.hoa_percent_increase_yearly: float = hoa_percent_increase_yearly
        self.insurance_percent_increase_yearly: float = (
            insurance_percent_increase_yearly
        )

        # --- Values calculated from user-provided details ---
        self.insurance_monthly: float = self.insurance_yearly / 12

        # --- Initializing values from the home purchase the rental is being compared to. The main script will update these values. ---
        self.years_in_house: float = 0
        self.months_in_house: int = 0
        self.initial_investment: float = 0

        # --- Initializing the dataframe to store all time-based metrics for the rental. The main script will update the dataframe. ---
        self.df_rent = pd.DataFrame(
            0.0,
            index=range(1, self.months_in_house + 1),
            columns=[
                "Rent",
                "HOA",
                "Rent insurance",
                "Total housing payment (28%)",
                "Investment balance",
                "Investment gains",
                "Investment deposited",
            ],
        )

        # --- Initializing investment related metrics. The main script will update these values. ---
        self.investment_gains_percent_yearly: float = 0
