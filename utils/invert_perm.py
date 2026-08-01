
def invert_perm(perm):
    ndim = len(perm)
    new_perm = [-1] * ndim
    for idx, x in enumerate(perm):
        new_perm[x] = idx
    return new_perm

