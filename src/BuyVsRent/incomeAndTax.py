class incomeAndTax:

    def __init__(
        self,
        income_yearly: int,
        income_percent_increase_yearly: float,
        federal_standard_deduction: int,
        federal_standard_deduction_percent_increase_yearly: float,
        federal_tax_brackets: dict[float, int],
        federal_maxes_percent_increase_yearly: float,
        state_standard_deduction: int,
        state_standard_deduction_percent_increase_yearly: float,
        state_tax_brackets: dict[float, int],
        state_maxes_percent_increase_yearly: float,
    ):

        self.income_yearly: int = income_yearly
        self.income_percent_increase_yearly: float = income_percent_increase_yearly

        self.federal_standard_deduction: int = federal_standard_deduction
        self.federal_standard_deduction_percent_increase_yearly: float = (
            federal_standard_deduction_percent_increase_yearly
        )
        self.federal_tax_brackets: dict[float, int] = federal_tax_brackets
        self.federal_maxes_percent_increase_yearly: float = (
            federal_maxes_percent_increase_yearly
        )

        self.state_standard_deduction: int = state_standard_deduction
        self.state_standard_deduction_percent_increase_yearly: float = (
            state_standard_deduction_percent_increase_yearly
        )
        self.state_tax_brackets: dict[float, int] = state_tax_brackets
        self.state_maxes_percent_increase_yearly: float = (
            state_maxes_percent_increase_yearly
        )

    def calculate_federal_tax(self, gross_income):

        tax = 0

        if gross_income >= self.federal_tax_brackets["10 % max"]:
            tax += self.federal_tax_brackets["10 % max"] * 0.10

            if gross_income > self.federal_tax_brackets["12 % max"]:
                tax += (
                    self.federal_tax_brackets["12 % max"]
                    - self.federal_tax_brackets["10 % max"]
                ) * 0.12

                if gross_income > self.federal_tax_brackets["22 % max"]:
                    tax += (
                        self.federal_tax_brackets["22 % max"]
                        - self.federal_tax_brackets["12 % max"]
                    ) * 0.22

                    if gross_income > self.federal_tax_brackets["24 % max"]:
                        tax += (
                            self.federal_tax_brackets["24 % max"]
                            - self.federal_tax_brackets["22 % max"]
                        ) * 0.24

                        if gross_income > self.federal_tax_brackets["32 % max"]:
                            tax += (
                                self.federal_tax_brackets["32 % max"]
                                - self.federal_tax_brackets["24 % max"]
                            ) * 0.32

                            if gross_income > self.federal_tax_brackets["35 % max"]:
                                tax += (
                                    self.federal_tax_brackets["35 % max"]
                                    - self.federal_tax_brackets["32 % max"]
                                ) * 0.35
                                tax += (
                                    gross_income - self.federal_tax_brackets["35 % max"]
                                ) * 0.37

                            else:
                                tax += (
                                    gross_income - self.federal_tax_brackets["32 % max"]
                                ) * 0.35
                        else:
                            tax += (
                                gross_income - self.federal_tax_brackets["24 % max"]
                            ) * 0.32
                    else:
                        tax += (
                            gross_income - self.federal_tax_brackets["22 % max"]
                        ) * 0.24
                else:
                    tax += (gross_income - self.federal_tax_brackets["12 % max"]) * 0.22
            else:
                tax += (gross_income - self.federal_tax_brackets["10 % max"]) * 0.12

        return tax

    def calculate_state_tax(self, gross_income):

        tax = 0

        if gross_income >= self.state_tax_brackets["2 % max"]:
            tax += self.state_tax_brackets["2 % max"] * 0.02

            if gross_income > self.state_tax_brackets["3 % max"]:
                tax += (
                    self.state_tax_brackets["3 % max"]
                    - self.state_tax_brackets["2 % max"]
                ) * 0.03

                if gross_income > self.state_tax_brackets["5 % max"]:
                    tax += (
                        self.state_tax_brackets["5 % max"]
                        - self.state_tax_brackets["3 % max"]
                    ) * 0.05
                    tax += (gross_income - self.state_tax_brackets["5 % max"]) * 0.0575

                else:
                    tax += (gross_income - self.state_tax_brackets["3 % max"]) * 0.05
            else:
                tax += (gross_income - self.state_tax_brackets["2 % max"]) * 0.03

        return tax
