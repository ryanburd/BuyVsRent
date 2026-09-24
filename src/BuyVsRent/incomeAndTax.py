import numpy as np
import pandas as pd


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
        loan_length_years: float = 30,
    ):

        # --- Values used by other class functions ---
        self.income_percent_increase_yearly: float = income_percent_increase_yearly
        self.federal_standard_deduction_percent_increase_yearly: float = (
            federal_standard_deduction_percent_increase_yearly
        )
        self.federal_tax_brackets: dict[float, int] = federal_tax_brackets
        self.federal_maxes_percent_increase_yearly: float = (
            federal_maxes_percent_increase_yearly
        )

        self.state_standard_deduction_percent_increase_yearly: float = (
            state_standard_deduction_percent_increase_yearly
        )
        self.state_tax_brackets: dict[float, int] = state_tax_brackets
        self.state_maxes_percent_increase_yearly: float = (
            state_maxes_percent_increase_yearly
        )

        # --- Values calculated from user-provided details ---
        loan_length_months: float = np.round(loan_length_years * 12, 0)

        # --- Create dataframe for YEARLY income and taxes each month ---
        self.df = pd.DataFrame(
            0.0,
            index=range(1, loan_length_months + 1),
            columns=[
                "Yearly income",
                "Federal standard deduction",
                "Federal standard gross income",
                "Yearly federal standard taxes",
                "Federal itemized deduction",
                "Federal itemized gross income",
                "Yearly federal itemized taxes",
                "10 % max",
                "12 % max",
                "22 % max",
                "24 % max",
                "32 % max",
                "35 % max",
                "37 % max",
                "State standard deduction",
                "State standard gross income",
                "Yearly state standard taxes",
                "2 % max",
                "3 % max",
                "5 % max",
                "5.75 % max",
            ],
        )

        # --- Initialize the first month of income and tax metrics ---
        self.df.loc[1, "Yearly income"] = income_yearly

        self.df.loc[1, "Federal standard deduction"] = federal_standard_deduction
        self.df.loc[1, "Federal standard gross income"] = (
            income_yearly - federal_standard_deduction
        )
        self.df.loc[1, "10 % max":"37 % max"] = self.federal_tax_brackets

        self.df.loc[1, "State standard deduction"] = state_standard_deduction
        self.df.loc[1, "State standard gross income"] = (
            income_yearly - state_standard_deduction
        )
        self.df.loc[1, "2 % max":"5.75 % max"] = self.state_tax_brackets

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

    def update_yearly_income(self, month):
        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "Yearly income"] = self.df.loc[
                month - 1, "Yearly income"
            ]
        else:
            self.df.loc[month, "Yearly income"] = self.df.loc[
                month - 1, "Yearly income"
            ] * (1 + self.income_percent_increase_yearly / 100)

    def update_yearly_federal_std_deduction(self, month):
        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "Federal standard deduction"] = self.df.loc[
                month - 1, "Federal standard deduction"
            ]
        else:
            self.df.loc[month, "Federal standard deduction"] = self.df.loc[
                month - 1, "Federal standard deduction"
            ] * (1 + self.federal_standard_deduction_percent_increase_yearly / 100)

    def update_yearly_federal_std_gross(self, month):
        self.df.loc[month, "Federal standard gross income"] = (
            self.df.loc[month, "Yearly income"]
            - self.df.loc[month, "Federal standard deduction"]
        )

    def update_yearly_federal_brackets(self, month):
        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "10 % max":"37 % max"] = self.df.loc[
                month - 1, "10 % max":"37 % max"
            ]
        else:
            self.df.loc[month, "10 % max":"37 % max"] = self.df.loc[
                month - 1, "10 % max":"37 % max"
            ] * (1 + self.federal_maxes_percent_increase_yearly / 100)

    def update_yearly_federal_std_taxes(self, month):
        self.df.loc[month, "Yearly federal standard taxes"] = (
            self.calculate_federal_tax(
                self.df.loc[month, "Federal standard gross income"]
            )
        )

    def update_yearly_state_std_deduction(self, month):
        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "State standard deduction"] = self.df.loc[
                month - 1, "State standard deduction"
            ]
        else:
            self.df.loc[month, "State standard deduction"] = self.df.loc[
                month - 1, "State standard deduction"
            ] * (1 + self.state_standard_deduction_percent_increase_yearly / 100)

    def update_yearly_state_std_gross(self, month):
        self.df.loc[month, "State standard gross income"] = (
            self.df.loc[month, "Yearly income"]
            - self.df.loc[month, "State standard deduction"]
        )

    def update_yearly_state_brackets(self, month):
        if np.mod(month - 1, 12) != 0:
            self.df.loc[month, "2 % max":"5.75 % max"] = self.df.loc[
                month - 1, "2 % max":"5.75 % max"
            ]
        else:
            self.df.loc[month, "2 % max":"5.75 % max"] = self.df.loc[
                month - 1, "2 % max":"5.75 % max"
            ] * (1 + self.state_maxes_percent_increase_yearly / 100)

    def update_yearly_state_std_taxes(self, month):
        self.df.loc[month, "Yearly state standard taxes"] = self.calculate_state_tax(
            self.df.loc[month, "State standard gross income"]
        )

    def update_first_month_taxes(self):
        self.df.loc[1, "Yearly federal standard taxes"] = self.df.loc[
            2, "Yearly federal standard taxes"
        ]
        self.df.loc[1, "Yearly state standard taxes"] = self.df.loc[
            2, "Yearly state standard taxes"
        ]

    def calculate_yearly_federal_item_deduction(self, buyer):
        self.df["Federal itemized deduction"] = (
            buyer.df["Itemizable expenses"]
            .groupby(np.arange(len(buyer.df)) // 12)
            .transform("sum")
        )

    def calculate_yearly_federal_item_gross(self):
        self.df["Federal itemized gross income"] = (
            self.df["Yearly income"] - self.df["Federal itemized deduction"]
        )

    def calculate_yearly_federal_item_taxes(self):
        self.df["Yearly federal itemized taxes"] = self.df[
            "Federal itemized gross income"
        ].apply(self.calculate_federal_tax)
