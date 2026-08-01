
def dup_sqf_norm(f, K):
    r"""
    Find a shift of `f` in `K[x]` that has square-free norm.

    The domain `K` must be an algebraic number field `k(a)` (see :ref:`QQ(a)`).

    Returns `(s,g,r)`, such that `g(x)=f(x-sa)`, `r(x)=\text{Norm}(g(x))` and
    `r` is a square-free polynomial over `k`.

    Examples
    ========

    We first create the algebraic number field `K=k(a)=\mathbb{Q}(\sqrt{3})`
    and rings `K[x]` and `k[x]`:

    >>> from sympy.polys import ring, QQ
    >>> from sympy import sqrt

    >>> K = QQ.algebraic_field(sqrt(3))
    >>> R, x = ring("x", K)
    >>> _, X = ring("x", QQ)

    We can now find a square free norm for a shift of `f`:

    >>> f = x**2 - 1
    >>> s, g, r = R.dup_sqf_norm(f)

    The choice of shift `s` is arbitrary and the particular values returned for
    `g` and `r` are determined by `s`.

    >>> s == 1
    True
    >>> g == x**2 - 2*sqrt(3)*x + 2
    True
    >>> r == X**4 - 8*X**2 + 4
    True

    The invariants are:

    >>> g == f.shift(-s*K.unit)
    True
    >>> g.norm() == r
    True
    >>> r.is_squarefree
    True

    Explanation
    ===========

    This is part of Trager's algorithm for factorizing polynomials over
    algebraic number fields. In particular this function is algorithm
    ``sqfr_norm`` from [Trager76]_.

    See Also
    ========

    dmp_sqf_norm:
        Analogous function for multivariate polynomials over ``k(a)``.
    dmp_norm:
        Computes the norm of `f` directly without any shift.
    dup_ext_factor:
        Function implementing Trager's algorithm that uses this.
    sympy.polys.polytools.sqf_norm:
        High-level interface for using this function.
    """
    if not K.is_Algebraic:
        raise DomainError("ground domain must be algebraic")

    s, g = 0, dmp_raise(K.mod.to_list(), 1, 0, K.dom)

    while True:
        h, _ = dmp_inject(f, 0, K, front=True)
        r = dmp_resultant(g, h, 1, K.dom)

        if dup_sqf_p(r, K.dom):
            break
        else:
            f, s = dup_shift(f, -K.unit, K), s + 1

    return s, f, r

