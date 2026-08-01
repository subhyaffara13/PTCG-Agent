
def dmp_norm(f, u, K):
    r"""
    Norm of ``f`` in ``K[X]``, often not square-free.

    The domain `K` must be an algebraic number field `k(a)` (see :ref:`QQ(a)`).

    Examples
    ========

    We first define the algebraic number field `K = k(a) = \mathbb{Q}(\sqrt{2})`:

    >>> from sympy import QQ, sqrt
    >>> from sympy.polys.sqfreetools import dmp_norm
    >>> k = QQ
    >>> K = k.algebraic_field(sqrt(2))

    We can now compute the norm of a polynomial `p` in `K[x,y]`:

    >>> p = [[K(1)], [K(1),K.unit]]                  # x + y + sqrt(2)
    >>> N = [[k(1)], [k(2),k(0)], [k(1),k(0),k(-2)]] # x**2 + 2*x*y + y**2 - 2
    >>> dmp_norm(p, 1, K) == N
    True

    In higher level functions that is:

    >>> from sympy import expand, roots, minpoly
    >>> from sympy.abc import x, y
    >>> from math import prod
    >>> a = sqrt(2)
    >>> e = (x + y + a)
    >>> e.as_poly([x, y], extension=a).norm()
    Poly(x**2 + 2*x*y + y**2 - 2, x, y, domain='QQ')

    This is equal to the product of the expressions `x + y + a_i` where the
    `a_i` are the conjugates of `a`:

    >>> pa = minpoly(a)
    >>> pa
    _x**2 - 2
    >>> rs = roots(pa, multiple=True)
    >>> rs
    [sqrt(2), -sqrt(2)]
    >>> n = prod(e.subs(a, r) for r in rs)
    >>> n
    (x + y - sqrt(2))*(x + y + sqrt(2))
    >>> expand(n)
    x**2 + 2*x*y + y**2 - 2

    Explanation
    ===========

    Given an algebraic number field `K = k(a)` any element `b` of `K` can be
    represented as polynomial function `b=g(a)` where `g` is in `k[x]`. If the
    minimal polynomial of `a` over `k` is `p_a` then the roots `a_1`, `a_2`,
    `\cdots` of `p_a(x)` are the conjugates of `a`. The norm of `b` is the
    product `g(a1) \times g(a2) \times \cdots` and is an element of `k`.

    As in [Trager76]_ we extend this norm to multivariate polynomials over `K`.
    If `b(x)` is a polynomial in `k(a)[X]` then we can think of `b` as being
    alternately a function `g_X(a)` where `g_X` is an element of `k[X][y]` i.e.
    a polynomial function with coefficients that are elements of `k[X]`. Then
    the norm of `b` is the product `g_X(a1) \times g_X(a2) \times \cdots` and
    will be an element of `k[X]`.

    See Also
    ========

    dmp_sqf_norm:
        Compute a shift of `f` so that the `\text{Norm}(f)` is square-free.
    sympy.polys.polytools.Poly.norm:
        Higher-level function that calls this.
    """
    if not K.is_Algebraic:
        raise DomainError("ground domain must be algebraic")

    g = dmp_raise(K.mod.to_list(), u + 1, 0, K.dom)
    h, _ = dmp_inject(f, u, K, front=True)

    return dmp_resultant(g, h, u + 1, K.dom)

