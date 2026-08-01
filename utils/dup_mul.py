
def dup_mul(f, g, K):
    """
    Multiply dense polynomials in ``K[x]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_mul(x - 2, x + 2)
    x**2 - 4

    """
    if f == g:
        return dup_sqr(f, K)

    if not (f and g):
        return []

    df = dup_degree(f)
    dg = dup_degree(g)

    n = max(df, dg) + 1

    if n < 100 or not K.is_Exact:
        h = []

        for i in range(0, df + dg + 1):
            coeff = K.zero

            for j in range(max(0, i - dg), min(df, i) + 1):
                coeff += f[j]*g[i - j]

            h.append(coeff)

        return dup_strip(h)
    else:
        # Use Karatsuba's algorithm (divide and conquer), see e.g.:
        # Joris van der Hoeven, Relax But Don't Be Too Lazy,
        # J. Symbolic Computation, 11 (2002), section 3.1.1.
        n2 = n//2

        fl, gl = dup_slice(f, 0, n2, K), dup_slice(g, 0, n2, K)

        fh = dup_rshift(dup_slice(f, n2, n, K), n2, K)
        gh = dup_rshift(dup_slice(g, n2, n, K), n2, K)

        lo, hi = dup_mul(fl, gl, K), dup_mul(fh, gh, K)

        mid = dup_mul(dup_add(fl, fh, K), dup_add(gl, gh, K), K)
        mid = dup_sub(mid, dup_add(lo, hi, K), K)

        return dup_add(dup_add(lo, dup_lshift(mid, n2, K), K),
                       dup_lshift(hi, 2*n2, K), K)

