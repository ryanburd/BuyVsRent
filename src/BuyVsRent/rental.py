import numpy as np


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

        # --- Values calculated from user-pprovided details ---
        self.insurance_monthly: float = self.insurance_yearly / 12

        # --- Initializing values to be updated later ---
        self.investment_gains_percent_yearly: float = 0

        # --- Initializing values to be updated each month or year ---
        self.current_month_rent: float = 0
        self.current_month_hoa: float = 0
        self.current_month_insurance: float = 0
        self.current_month_payment: float = 0

        # --- Initializing arrays to store time-based data ---
        self.investment_balance = np.zeros(1)
