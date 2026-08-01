
def _find_missing_index(ind, n):
    for k, a in enumerate(ind):
        if k != a:
            return k

    k += 1
    if k < n:
        return k
    else:
        return -1

