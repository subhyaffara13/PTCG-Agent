
def fprati(p1, f1, p2, f2, p3, f3):
    """The root of r(p) = (u*p + v) / (p + w) given three points and values,
    (p1, f2), (p2, f2) and (p3, f3).

    The FITPACK analog adjusts the bounds, and we do not
    https://github.com/scipy/scipy/blob/maintenance/1.11.x/scipy/interpolate/fitpack/fprati.f

    NB: FITPACK uses p < 0 to encode p=infinity. We just use the infinity itself.
    Since the bracket is ``p1 <= p2 <= p3``, ``p3`` can be infinite (in fact,
    this is what the minimizer starts with, ``p3=inf``).
    """
    h1 = f1 * (f2 - f3)
    h2 = f2 * (f3 - f1)
    h3 = f3 * (f1 - f2)
    if p3 == np.inf:
        return -(p2*h1 + p1*h2) / h3
    return -(p1*p2*h3 + p2*p3*h1 + p1*p3*h2) / (p1*h1 + p2*h2 + p3*h3)

