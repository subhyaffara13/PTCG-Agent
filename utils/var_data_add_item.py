
def VarData_addItem(self, deltas, *, round=round):
    deltas = [round(d) for d in deltas]

    countUs = self.VarRegionCount
    countThem = len(deltas)
    if countUs + 1 == countThem:
        deltas = list(deltas[1:])
    else:
        assert countUs == countThem, (countUs, countThem)
        deltas = list(deltas)
    self.Item.append(deltas)
    self.ItemCount = len(self.Item)

