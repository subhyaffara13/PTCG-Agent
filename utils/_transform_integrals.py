
def _transform_integrals(a, b, xp):
    # Transform integrals to a form with finite a <= b
    # For b == a (even infinite), we ensure that the limits remain equal
    # For b < a, we reverse the limits and will multiply the final result by -1
    # For infinite limit on the right, we use the substitution x = 1/t - 1 + a
    # For infinite limit on the left, we substitute x = -x and treat as above
    # For infinite limits, we substitute x = t / (1-t**2)
    ab_same = (a == b)
    a[ab_same], b[ab_same] = 1, 1

    # `a, b` may have complex dtype but have zero imaginary part
    negative = xp.real(b) < xp.real(a)
    a[negative], b[negative] = b[negative], a[negative]

    abinf = xp.isinf(a) & xp.isinf(b)
    a[abinf], b[abinf] = -1, 1

    ainf = xp.isinf(a)
    a[ainf], b[ainf] = -b[ainf], -a[ainf]

    binf = xp.isinf(b)
    a0 = xp_copy(a)
    a[binf], b[binf] = 0, 1

    return a, b, a0, negative, abinf, ainf, binf

