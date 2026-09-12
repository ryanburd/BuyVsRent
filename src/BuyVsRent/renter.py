class renter:

    def __init__(
        self,
        rent_monthly,
        hoa_monthly,
        insurance_yearly,
        rent_percent_increase_yearly=3,
        insurance_percent_increase_yearly=5,
        investment_gains_percent_yearly=8,
    ):

        # --- User-provided details with no default value ---
        self.rent_monthly = rent_monthly
        self.hoa_monthly = hoa_monthly
        self.insurance_yearly = insurance_yearly

        # --- Details with a default value. The user can override the default by providing a value ---
        self.rent_percent_increase_yearly = rent_percent_increase_yearly
        self.insurance_percent_increase_yearly = insurance_percent_increase_yearly
        self.investment_gains_percent_yearly = investment_gains_percent_yearly

        # --- Values calculated from user-pprovided details ---
        self.insurance_monthly = self.insurance_yearly / 12

        # --- Initializing assets at 0 ---
        self.investment_balance = 0
