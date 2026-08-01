
def dumeq(i, j):
    if type(i) in (list, tuple):
        return all(dumeq(i, j) for i, j in zip(i, j))
    return i == j or i.dummy_eq(j)

