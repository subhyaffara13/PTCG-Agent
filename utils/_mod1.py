
def _mod1(x):
    # TODO see if this can work as Mod(x, 1); this will require
    # different handling of the "buckets" since these need to
    # be sorted and that fails when there is a mixture of
    # integers and expressions with parameters. With the current
    # Mod behavior, Mod(k, 1) == Mod(1, 1) == 0 if k is an integer.
    # Although the sorting can be done with Basic.compare, this may
    # still require different handling of the sorted buckets.
    if x.is_Number:
        return Mod(x, 1)
    c, x = x.as_coeff_Add()
    return Mod(c, 1) + x

