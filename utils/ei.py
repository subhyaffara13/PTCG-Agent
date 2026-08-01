
def ei(z, _e1=False):
    typez = type(z)
    if typez not in (float, complex):
        try:
            z = float(z)
            typez = float
        except (TypeError, ValueError):
            z = complex(z)
            typez = complex
    if not z:
        return -INF
    absz = abs(z)
    if absz > EI_ASYMP_CONVERGENCE_RADIUS:
        return ei_asymp(z, _e1)
    elif absz <= 2.0 or (typez is float and z > 0.0):
        return ei_taylor(z, _e1)
    # Integrate, starting from whichever is smaller of a Taylor
    # series value or an asymptotic series value
    if typez is complex and z.real > 0.0:
        zref = z / absz
        ref = ei_taylor(zref, _e1)
    else:
        zref = EI_ASYMP_CONVERGENCE_RADIUS * z / absz
        ref = ei_asymp(zref, _e1)
    C = (zref-z)*0.5
    D = (zref+z)*0.5
    s = 0.0
    if type(z) is complex:
        _exp = cmath.exp
    else:
        _exp = math.exp
    for x,w in gauss42:
        t = C*x+D
        s += w*_exp(t)/t
    ref -= C*s
    return ref


def ei(ctx, z):
    try:
        return ctx._ei(z)
    except NotImplementedError:
        return ctx._ei_generic(z)

