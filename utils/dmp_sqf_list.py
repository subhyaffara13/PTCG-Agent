
def dmp_sqf_list(f, u, K, all=False):
    """
    Return square-free decomposition of a polynomial in `K[X]`.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> f = x**5 + 2*x**4*y + x**3*y**2

    >>> R.dmp_sqf_list(f)
    (1, [(x + y, 2), (x, 3)])
    >>> R.dmp_sqf_list(f, all=True)
    (1, [(1, 1), (x + y, 2), (x, 3)])

    Explanation
    ===========

    Uses Yun's algorithm for univariate polynomials from [Yun76]_ recursively.
    The multivariate polynomial is treated as a univariate polynomial in its
    leading variable. Then Yun's algorithm computes the square-free
    factorization of the primitive and the content is factored recursively.

    It would be better to use a dedicated algorithm for multivariate
    polynomials instead.

    See Also
    ========

    dup_sqf_list:
        Corresponding function for univariate polynomials.
    sympy.polys.polytools.sqf_list:
        High-level function for square-free factorization of expressions.
    sympy.polys.polytools.Poly.sqf_list:
        Analogous method on :class:`~.Poly`.
    """
    if not u:
        return dup_sqf_list(f, K, all=all)

    if K.is_FiniteField:
        return dmp_gf_sqf_list(f, u, K, all=all)

    f_orig = f

    if K.is_Field:
        coeff = dmp_ground_LC(f, u, K)
        f = dmp_ground_monic(f, u, K)
    else:
        coeff, f = dmp_ground_primitive(f, u, K)

        if K.is_negative(dmp_ground_LC(f, u, K)):
            f = dmp_neg(f, u, K)
            coeff = -coeff

    deg = dmp_degree(f, u)
    if deg < 0:
        return coeff, []

    # Yun's algorithm requires the polynomial to be primitive as a univariate
    # polynomial in its main variable.
    content, f = dmp_primitive(f, u, K)

    result = {}

    if deg != 0:

        h = dmp_diff(f, 1, u, K)
        g, p, q = dmp_inner_gcd(f, h, u, K)

        i = 1

        while True:
            d = dmp_diff(p, 1, u, K)
            h = dmp_sub(q, d, u, K)

            if dmp_zero_p(h, u):
                result[i] = p
                break

            g, p, q = dmp_inner_gcd(p, h, u, K)

            if all or dmp_degree(g, u) > 0:
                result[i] = g

            i += 1

    coeff_content, result_content = dmp_sqf_list(content, u-1, K, all=all)

    coeff *= coeff_content

    # Combine factors of the content and primitive part that have the same
    # multiplicity to produce a list in ascending order of multiplicity.
    for fac, i in result_content:
        fac = [fac]
        if i in result:
            result[i] = dmp_mul(result[i], fac, u, K)
        else:
            result[i] = fac

    result = [(result[i], i) for i in sorted(result)]

    _dmp_check_degrees(f_orig, u, result)

    return coeff, result

