from src.engine.types.Ratios import Ratios
from src.engine.types.Basics import Basics
from src.engine.types.IncomeChanges import IncomeChanges
from src.engine.types.BalanceSheetChanges import BalanceSheetChanges
from src.engine.types.CashFlowChanges import CashFlowChanges
from src.engine.types.DiscountedCashFlow import DiscountedCashFlow

class Decide:
    parent = ""
    subsector = ""
    type = ""
    data = []

    def __init__(self, parent, subsector, type, data):
        self.parent = parent
        self.subsector = subsector
        self.type = type
        self.data = data

    def final(self):
        if self.type == 'ratios':
            return Ratios(self.parent, self.subsector, self.data).final()
        elif self.type == 'basics':
            return Basics(self.parent, self.subsector, self.data).final()
        elif self.type == 'incomechanges':
            return IncomeChanges(self.parent, self.subsector, self.data).final()
        elif self.type == 'balancesheetchanges':
            return BalanceSheetChanges(self.parent, self.subsector, self.data).final()
        elif self.type == 'cashflowchanges':
            return CashFlowChanges(self.parent, self.subsector, self.data).final()
        elif self.type == 'discountedcashflow':
            return DiscountedCashFlow(self.parent, self.subsector, self.data).final()
        else:
            return "[]"