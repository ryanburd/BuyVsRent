class buyer:

    def __init__(
        self,
        purchase_price,
        down_payment_percent,
        interest_APR_yearly,
        hoa_monthly,
        tax_percent_yearly=1,
        insurance_monthly=150,
        insurance_percent_increase_yearly=5,
        pmi_percent_yearly=1,
        maintenance_percent_yearly=1,
        buying_costs_percent=4,
        selling_costs_percent=6,
        appreciation_percent_yearly=2,
        investment_gains_percent_yearly=8,
    ):

        # --- User-provided details with no default value ---
        self.purchase_price = purchase_price
        self.down_payment_percent = down_payment_percent
        self.interest_APR_yearly = interest_APR_yearly
        self.hoa_monthly = hoa_monthly

        # --- Details with default values. The user can override the defaul by providing a value ---
        self.tax_percent_yearly = tax_percent_yearly
        self.insurance_monthly = insurance_monthly
        self.insurance_percent_increase_yearly = insurance_percent_increase_yearly
        self.pmi_percent_yearly = pmi_percent_yearly
        self.maintenance_percent_yearly = maintenance_percent_yearly
        self.buying_costs_percent = buying_costs_percent
        self.selling_costs_percent = selling_costs_percent
        self.appreciation_percent_yearly = appreciation_percent_yearly
        self.investment_gains_percent_yearly = investment_gains_percent_yearly

        # --- Values calculated from the user-provided details ---
        self.down_payment = self.purchase_price * self.down_payment_percent / 100
        self.initial_loan_balance = self.purchase_price - self.down_payment
        self.no_pmi_balance = self.purchase_price * 0.8
        self.interest_rate_monthly = self.interest_APR_yearly / 100 / 12
        self.pi_monthly = (
            self.initial_loan_balance
            * self.interest_rate_monthly
            * (1 + self.interest_rate_monthly) ** 360
            / ((1 + self.interest_rate_monthly) ** 360 - 1)
        )

        # --- Initializing assets at 0 ---
        self.equity = 0
        self.investment_balance = 0
