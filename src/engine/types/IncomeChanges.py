class IncomeChanges:
    parent = ""
    subsector = ""
    data = []

    def __init__(self, parent, subsector, data):
        self.parent = parent
        self.subsector = subsector
        self.data = data

    def final(self):
        print("From Income changes")
        print(self.parent)
        print(self.subsector)
        return ""

