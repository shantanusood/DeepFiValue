class DiscountedCashFlow:
    parent = ""
    subsector = ""
    data = []

    def __init__(self, parent, subsector, data):
        self.parent = parent
        self.subsector = subsector
        self.data = data

    def final(self):
        print("From Discount")
        print(self.parent)
        print(self.subsector)
        return str(self.data).replace("'", "\"")


#We need 3 things for doing this calculations:
#   1. Free cash flow projections
#   2. WACC (weighted average cost of capital) & Perpectual growth rate of free cash flow (2.5%)
#   3. Terminal value