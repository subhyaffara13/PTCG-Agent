
def update_sets(seq, atoms, func):
    s = set(seq)
    s = atoms.intersection(s)
    new = atoms - s
    s.update(list(filter(func, new)))
    return list(s)

