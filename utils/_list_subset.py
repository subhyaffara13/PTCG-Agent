
def _list_subset(l, indices):
    count = len(l)
    return [l[i] for i in indices if i < count]

