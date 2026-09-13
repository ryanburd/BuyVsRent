class purchase:

    def __init__(
        self,
        purchase_price: int,
        down_payment_percent: float,
        interest_APR_yearly: float,
        hoa_monthly: float,
        loan_length_years: int = 30,
        hoa_percent_increase_yearly: float = 3,
        tax_percent_yearly: float = 1,
        tax_percent_increase_yearly: float = 1,
        insurance_monthly: int = 150,
        insurance_percent_increase_yearly: float = 5,
        pmi_percent_yearly: float = 1,
        maintenance_percent_yearly: float = 1,
        buying_costs_percent: float = 4,
        selling_costs_percent: float = 6,
        appreciation_percent_yearly: float = 2,
    ):

        # --- User-provided details with no default value ---
        self.purchase_price: int = purchase_price
        self.down_payment_percent: float = down_payment_percent
        self.interest_APR_yearly: float = interest_APR_yearly
        self.hoa_monthly: float = hoa_monthly

        # --- Details with default values. The user can override the defaul by providing a value ---
        self.loan_length_years: int = loan_length_years
        self.hoa_percent_increase_yearly: float = hoa_percent_increase_yearly
        self.tax_percent_yearly: float = tax_percent_yearly
        self.tax_percent_increase_yearly: float = tax_percent_increase_yearly
        self.insurance_monthly: int = insurance_monthly
        self.insurance_percent_increase_yearly: float = (
            insurance_percent_increase_yearly
        )
        self.pmi_percent_yearly: float = pmi_percent_yearly
        self.maintenance_percent_yearly: float = maintenance_percent_yearly
        self.buying_costs_percent: float = buying_costs_percent
        self.selling_costs_percent: float = selling_costs_percent
        self.appreciation_percent_yearly: float = appreciation_percent_yearly

        # --- Values calculated from the user-provided details ---
        self.down_payment: float = self.purchase_price * self.down_payment_percent / 100
        self.initial_loan_balance: float = self.purchase_price - self.down_payment
        self.no_pmi_balance: float = self.purchase_price * 0.8
        self.interest_rate_monthly: float = self.interest_APR_yearly / 100 / 12
        self.pi_monthly: float = (
            self.initial_loan_balance
            * self.interest_rate_monthly
            * (1 + self.interest_rate_monthly) ** (self.loan_length_years * 12)
            / ((1 + self.interest_rate_monthly) ** (self.loan_length_years * 12) - 1)
        )
        self.equity: float = self.down_payment
        self.buying_costs = self.purchase_price * self.buying_costs_percent

        # --- Initializing values to be updated later ---
        self.investment_balance: float = 0
        self.investment_gains_percent_yearly: float = 0
