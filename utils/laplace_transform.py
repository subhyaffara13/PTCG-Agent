
def laplace_transform(f, t, s, legacy_matrix=True, **hints):
    r"""
    Compute the Laplace Transform `F(s)` of `f(t)`,

    .. math :: F(s) = \int_{0^{-}}^\infty e^{-st} f(t) \mathrm{d}t.

    Explanation
    ===========

    For all sensible functions, this converges absolutely in a
    half-plane

    .. math :: a < \operatorname{Re}(s)

    This function returns ``(F, a, cond)`` where ``F`` is the Laplace
    transform of ``f``, `a` is the half-plane of convergence, and `cond` are
    auxiliary convergence conditions.

    The implementation is rule-based, and if you are interested in which
    rules are applied, and whether integration is attempted, you can switch
    debug information on by setting ``sympy.SYMPY_DEBUG=True``. The numbers
    of the rules in the debug information (and the code) refer to Bateman's
    Tables of Integral Transforms [1].

    The lower bound is `0-`, meaning that this bound should be approached
    from the lower side. This is only necessary if distributions are involved.
    At present, it is only done if `f(t)` contains ``DiracDelta``, in which
    case the Laplace transform is computed implicitly as

    .. math ::
        F(s) = \lim_{\tau\to 0^{-}} \int_{\tau}^\infty e^{-st}
        f(t) \mathrm{d}t

    by applying rules.

    If the Laplace transform cannot be fully computed in closed form, this
    function returns expressions containing unevaluated
    :class:`LaplaceTransform` objects.

    For a description of possible hints, refer to the docstring of
    :func:`sympy.integrals.transforms.IntegralTransform.doit`. If
    ``noconds=True``, only `F` will be returned (i.e. not ``cond``, and also
    not the plane ``a``).

    .. deprecated:: 1.9
        Legacy behavior for matrices where ``laplace_transform`` with
        ``noconds=False`` (the default) returns a Matrix whose elements are
        tuples. The behavior of ``laplace_transform`` for matrices will change
        in a future release of SymPy to return a tuple of the transformed
        Matrix and the convergence conditions for the matrix as a whole. Use
        ``legacy_matrix=False`` to enable the new behavior.

    Examples
    ========

    >>> from sympy import DiracDelta, exp, laplace_transform
    >>> from sympy.abc import t, s, a
    >>> laplace_transform(t**4, t, s)
    (24/s**5, 0, True)
    >>> laplace_transform(t**a, t, s)
    (gamma(a + 1)/(s*s**a), 0, re(a) > -1)
    >>> laplace_transform(DiracDelta(t)-a*exp(-a*t), t, s, simplify=True)
    (s/(a + s), -re(a), True)

    There are also helper functions that make it easy to solve differential
    equations by Laplace transform. For example, to solve

    .. math :: m x''(t) + d x'(t) + k x(t) = 0

    with initial value `0` and initial derivative `v`:

    >>> from sympy import Function, laplace_correspondence, diff, solve
    >>> from sympy import laplace_initial_conds, inverse_laplace_transform
    >>> from sympy.abc import d, k, m, v
    >>> x = Function('x')
    >>> X = Function('X')
    >>> f = m*diff(x(t), t, 2) + d*diff(x(t), t) + k*x(t)
    >>> F = laplace_transform(f, t, s, noconds=True)
    >>> F = laplace_correspondence(F, {x: X})
    >>> F = laplace_initial_conds(F, t, {x: [0, v]})
    >>> F
    d*s*X(s) + k*X(s) + m*(s**2*X(s) - v)
    >>> Xs = solve(F, X(s))[0]
    >>> Xs
    m*v/(d*s + k + m*s**2)
    >>> inverse_laplace_transform(Xs, s, t)
    2*v*exp(-d*t/(2*m))*sin(t*sqrt((-d**2 + 4*k*m)/m**2)/2)*Heaviside(t)/sqrt((-d**2 + 4*k*m)/m**2)

    References
    ==========

    .. [1] Erdelyi, A. (ed.), Tables of Integral Transforms, Volume 1,
           Bateman Manuscript Prooject, McGraw-Hill (1954), available:
           https://resolver.caltech.edu/CaltechAUTHORS:20140123-101456353

    See Also
    ========

    inverse_laplace_transform, mellin_transform, fourier_transform
    hankel_transform, inverse_hankel_transform

    """

    _noconds = hints.get('noconds', False)
    _simplify = hints.get('simplify', False)

    if isinstance(f, MatrixBase) and hasattr(f, 'applyfunc'):

        conds = not hints.get('noconds', False)

        if conds and legacy_matrix:
            adt = 'deprecated-laplace-transform-matrix'
            sympy_deprecation_warning(
                """
Calling laplace_transform() on a Matrix with noconds=False (the default) is
deprecated. Either noconds=True or use legacy_matrix=False to get the new
behavior.
                """,
                deprecated_since_version='1.9',
                active_deprecations_target=adt,
            )
            # Temporarily disable the deprecation warning for non-Expr objects
            # in Matrix
            with ignore_warnings(SymPyDeprecationWarning):
                return f.applyfunc(
                    lambda fij: laplace_transform(fij, t, s, **hints))
        else:
            elements_trans = [laplace_transform(
                fij, t, s, **hints) for fij in f]
            if conds:
                elements, avals, conditions = zip(*elements_trans)
                f_laplace = type(f)(*f.shape, elements)
                return f_laplace, Max(*avals), And(*conditions)
            else:
                return type(f)(*f.shape, elements_trans)

    LT, p, c = LaplaceTransform(f, t, s).doit(noconds=False,
                                              simplify=_simplify)

    if not _noconds:
        return LT, p, c
    else:
        return LT

