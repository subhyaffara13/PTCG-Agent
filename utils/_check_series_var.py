
def _check_series_var(p, x, name):
    index = p.ring.gens.index(x)
    m = min(p, key=lambda k: k[index])[index]
    if m < 0:
        raise PoleError("Asymptotic expansion of %s around [oo] not "
                        "implemented." % name)
    return index, m

