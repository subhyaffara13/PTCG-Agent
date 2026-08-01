
def _not_a_knot(x, k):
    """Given data x, construct the knot vector w/ not-a-knot BC.
    cf de Boor, XIII(12).

    For even k, it's a bit ad hoc: Greville sites + omit 2nd and 2nd-to-last
    data points, a la not-a-knot.
    This seems to match what Dierckx does, too:
    https://github.com/scipy/scipy/blob/maintenance/1.11.x/scipy/interpolate/fitpack/fpcurf.f#L63-L80
    """
    x = np.asarray(x)
    if k % 2 == 1:
        k2 = (k + 1) // 2
        t = x.copy()
    else:
        k2 = k // 2
        t = (x[1:] + x[:-1]) / 2

    t = t[k2:-k2]
    t = np.r_[(x[0],)*(k+1), t, (x[-1],)*(k+1)]
    return t

