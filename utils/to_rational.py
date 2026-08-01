
def to_rational(s, max_denom, limit=True):

    p, q = _mpmath_to_rational(s._mpf_)

    # Needed for GROUND_TYPES=flint if gmpy2 is installed because mpmath's
    # to_rational() function returns a gmpy2.mpz instance and if MPQ is
    # flint.fmpq then MPQ(p, q) will fail.
    p = int(p)
    q = int(q)

    if not limit or q <= max_denom:
        return p, q

    p0, q0, p1, q1 = 0, 1, 1, 0
    n, d = p, q

    while True:
        a = n//d
        q2 = q0 + a*q1
        if q2 > max_denom:
            break
        p0, q0, p1, q1 = p1, q1, p0 + a*p1, q2
        n, d = d, n - a*d

    k = (max_denom - q0)//q1

    number = MPQ(p, q)
    bound1 = MPQ(p0 + k*p1, q0 + k*q1)
    bound2 = MPQ(p1, q1)

    if not bound2 or not bound1:
        return p, q
    elif abs(bound2 - number) <= abs(bound1 - number):
        return bound2.numerator, bound2.denominator
    else:
        return bound1.numerator, bound1.denominator


def to_rational(s):
    """Convert a raw mpf to a rational number. Return integers (p, q)
    such that s = p/q exactly."""
    sign, man, exp, bc = s
    if sign:
        man = -man
    if bc == -1:
        raise ValueError("cannot convert %s to a rational number" % man)
    if exp >= 0:
        return man * (1<<exp), 1
    else:
        return man, 1<<(-exp)

