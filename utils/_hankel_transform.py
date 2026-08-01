
def _hankel_transform(f, r, k, nu, name, simplify=True):
    r"""
    Compute a general Hankel transform

    .. math:: F_\nu(k) = \int_{0}^\infty f(r) J_\nu(k r) r \mathrm{d} r.
    """
    F = integrate(f*besselj(nu, k*r)*r, (r, S.Zero, S.Infinity))

    if not F.has(Integral):
        return _simplify(F, simplify), S.true

    if not F.is_Piecewise:
        raise IntegralTransformError(name, f, 'could not compute integral')

    F, cond = F.args[0]
    if F.has(Integral):
        raise IntegralTransformError(name, f, 'integral in unexpected form')

    return _simplify(F, simplify), cond

