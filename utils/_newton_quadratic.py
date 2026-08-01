
def _newton_quadratic(ab, fab, d, fd, k):
    """Apply Newton-Raphson like steps, using divided differences to approximate f'

    ab is a real interval [a, b] containing a root,
    fab holds the real values of f(a), f(b)
    d is a real number outside [ab, b]
    k is the number of steps to apply
    """
    a, b = ab
    fa, fb = fab
    _, B, A = _compute_divided_differences([a, b, d], [fa, fb, fd],
                                           forward=True, full=False)

    # _P  is the quadratic polynomial through the 3 points
    def _P(x):
        # Horner evaluation of fa + B * (x - a) + A * (x - a) * (x - b)
        return (A * (x - b) + B) * (x - a) + fa

    if A == 0:
        r = a - fa / B
    else:
        r = (a if np.sign(A) * np.sign(fa) > 0 else b)
        # Apply k Newton-Raphson steps to _P(x), starting from x=r
        for i in range(k):
            r1 = r - _P(r) / (B + A * (2 * r - a - b))
            if not (ab[0] < r1 < ab[1]):
                if (ab[0] < r < ab[1]):
                    return r
                r = sum(ab) / 2.0
                break
            r = r1

    return r

