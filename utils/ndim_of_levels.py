
def ndim_of_levels(levels: Sequence[DimEntry]) -> int:
    r = 0
    for l in levels:
        if l.is_positional():
            r += 1
    return r

