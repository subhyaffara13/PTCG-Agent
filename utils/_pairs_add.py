
def _pairs_add(d, k, v):
    # Internal utility method for updating terms and factors data.
    c = d.get(k)
    if c is None:
        d[k] = v
    else:
        c = c + v
        if c:
            d[k] = c
        else:
            del d[k]

