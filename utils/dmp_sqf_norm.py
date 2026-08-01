
def dmp_sqf_norm(f, u, K):
    r"""
    Find a shift of ``f`` in ``K[X]`` that has square-free norm.

    The domain `K` must be an algebraic number field `k(a)` (see :ref:`QQ(a)`).

    Returns `(s,g,r)`, such that `g(x_1,x_2,\cdots)=f(x_1-s_1 a, x_2 - s_2 a,
    \cdots)`, `r(x)=\text{Norm}(g(x))` and `r` is a square-free polynomial over
    `k`.

    Examples
    ========

    We first create the algebraic number field `K=k(a)=\mathbb{Q}(i)` and rings
    `K[x,y]` and `k[x,y]`:

    >>> from sympy.polys import ring, QQ
    >>> from sympy import I

    >>> K = QQ.algebraic_field(I)
    >>> R, x, y = ring("x,y", K)
    >>> _, X, Y = ring("x,y", QQ)

    We can now find a square free norm for a shift of `f`:

    >>> f = x*y + y**2
    >>> s, g, r = R.dmp_sqf_norm(f)

    The choice of shifts ``s`` is arbitrary and the particular values returned
    for ``g`` and ``r`` are determined by ``s``.

    >>> s
    [0, 1]
    >>> g == x*y - I*x + y**2 - 2*I*y - 1
    True
    >>> r == X**2*Y**2 + X**2 + 2*X*Y**3 + 2*X*Y + Y**4 + 2*Y**2 + 1
    True

    The required invariants are:

    >>> g == f.shift_list([-si*K.unit for si in s])
    True
    >>> g.norm() == r
    True
    >>> r.is_squarefree
    True

    Explanation
    ===========

    This is part of Trager's algorithm for factorizing polynomials over
    algebraic number fields. In particular this function is a multivariate
    generalization of algorithm ``sqfr_norm`` from [Trager76]_.

    See Also
    ========

    dup_sqf_norm:
        Analogous function for univariate polynomials over ``k(a)``.
    dmp_norm:
        Computes the norm of `f` directly without any shift.
    dmp_ext_factor:
        Function implementing Trager's algorithm that uses this.
    sympy.polys.polytools.sqf_norm:
        High-level interface for using this function.
    """
    if not u:
        s, g, r = dup_sqf_norm(f, K)
        return [s], g, r

    if not K.is_Algebraic:
        raise DomainError("ground domain must be algebraic")

    g = dmp_raise(K.mod.to_list(), u + 1, 0, K.dom)

    for s, f in _dmp_sqf_norm_shifts(f, u, K):

        h, _ = dmp_inject(f, u, K, front=True)
        r = dmp_resultant(g, h, u + 1, K.dom)

        if dmp_sqf_p(r, u, K.dom):
            break

    return s, f, r

