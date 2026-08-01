
def MultiVarData_addItem(self, deltas, *, round=round):
    deltas = tuple(round(d) for d in deltas)

    assert len(deltas) == self.VarRegionCount

    values = []
    for d in deltas:
        values.extend(d)

    self.Item.append(values)
    self.ItemCount = len(self.Item)

