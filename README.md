## About this program

This program compares the value of the appreciating assets of buying a home vs renting a home.

## How it works

- Each month, both the buyer and renter start with the same amount of money, which equals the higher of the two total monthly payments.
- For the buyer, the total monthly payment includes:
    - Principal
    - Interest
    - Tax
    - Homeowner's insurance
    - HOA fee
    - PMI
    - Maintence costs
    - Federal taxes
- For the renter, the total monthly payment includes:
    - Rent
    - Renter's insurance
    - HOA fee
    - Federal taxes
- For the person (buyer or renter) who has the lower total payment for the month, the excess money is invested.
- The buyer's asset = equity + investment balance
- The renter's asset = investment balance
- The program shows both people's asset value vs year to compare which asset is worth more over time.
- The program also shows the net asset value if the person were to sell the asset after X months. This is often the more important metric to compare since both assets are only potential gains until the person sells the asset, which has an associated cost and tax implication.
- The monthly total homeowning payment and chargeable rent is plotted to show if and when there can be a cashflow for continuing to own the home and renting it out.

## To be included

- How receiving a family loan impacts the asset value of the buyer over time. The down payment increases (but the renter doesn't get to invest this portion), but the buyer now has to pay back this loan each month as well.
- The mortage+maintenance vs chargeable rent plot does not consider how the buyer's net asset value is changing once they start renting out the home. Even if cashflow is negative for the buyer, their net assets value can still be increasing due to increasing equity.

## Not included

- Utility costs

## Installation

Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install required packages:
```bash
pip install -r requirements.txt
```


