class taxBrackets:

    def __init__(
        self,
        standard_deduction: int,
        standard_deduction_percent_increase_yearly: float,
        bracket_maxes_married_jointly: dict[float, int],
        bracket_maxes_percent_increase_yearly: float,
    ):

        self.standard_deduction: int = standard_deduction
        self.standard_deduction_percent_increase_yearly: float = (
            standard_deduction_percent_increase_yearly
        )
        self.bracket_maxes_married_jointly: dict[float, int] = (
            bracket_maxes_married_jointly
        )
        self.bracket_maxes_percent_increase_yearly: float = (
            bracket_maxes_percent_increase_yearly
        )
