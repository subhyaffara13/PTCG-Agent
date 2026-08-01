
def _csolve_prime_las_vegas(f, p, seed=None):
    r""" Solutions of `f(x) \equiv 0 \pmod{p}`, `f(0) \not\equiv 0 \pmod{p}`.

    Explanation
    ===========

    This algorithm is classified as the Las Vegas method.
    That is, it always returns the correct answer and solves the problem
    fast in many cases, but if it is unlucky, it does not answer forever.

    Suppose the polynomial f is not a zero polynomial. Assume further
    that it is of degree at most p-1 and `f(0)\not\equiv 0 \pmod{p}`.
    These assumptions are not an essential part of the algorithm,
    only that it is more convenient for the function calling this
    function to resolve them.

    Note that `x^{p-1} - 1 \equiv \prod_{a=1}^{p-1}(x - a) \pmod{p}`.
    Thus, the greatest common divisor with f is `\prod_{s \in S}(x - s)`,
    with S being the set of solutions to f. Furthermore,
    when a is randomly determined, `(x+a)^{(p-1)/2}-1` is
    a polynomial with (p-1)/2 randomly chosen solutions.
    The greatest common divisor of f may be a nontrivial factor of f.

    When p is large and the degree of f is small,
    it is faster than naive solution methods.

    Parameters
    ==========

    f : polynomial
    p : prime number

    Returns
    =======

    list[int]
        a list of solutions, sorted in ascending order
        by integers in the range [1, p). The same value
        does not exist in the list even if there is
        a multiple solution. If no solution exists, returns [].

    Examples
    ========

    >>> from sympy.polys.galoistools import _csolve_prime_las_vegas
    >>> _csolve_prime_las_vegas([1, 4, 3], 7) # x^2 + 4x + 3 = 0 (mod 7)
    [4, 6]
    >>> _csolve_prime_las_vegas([5, 7, 1, 9], 11) # 5x^3 + 7x^2 + x + 9 = 0 (mod 11)
    [1, 5, 8]

    References
    ==========

    .. [1] R. Crandall and C. Pomerance "Prime Numbers", 2nd Ed., Algorithm 2.3.10

    """
    from sympy.polys.domains import ZZ
    from sympy.ntheory import sqrt_mod
    randint = _randint(seed)
    root = set()
    g = gf_pow_mod([1, 0], p - 1, f, p, ZZ)
    g = gf_sub_ground(g, 1, p, ZZ)
    # We want to calculate gcd(x**(p-1) - 1, f(x))
    factors = [gf_gcd(f, g, p, ZZ)]
    while factors:
        f = factors.pop()
        # If the degree is small, solve directly
        if len(f) <= 1:
            continue
        if len(f) == 2:
            root.add(-invert(f[0], p) * f[1] % p)
            continue
        if len(f) == 3:
            inv = invert(f[0], p)
            b = f[1] * inv % p
            b = (b + p * (b % 2)) // 2
            root.update((r - b) % p for r in
                        sqrt_mod(b**2 - f[2] * inv, p, all_roots=True))
            continue
        while True:
            # Determine `a` randomly and
            # compute gcd((x+a)**((p-1)//2)-1, f(x))
            a = randint(0, p - 1)
            g = gf_pow_mod([1, a], (p - 1) // 2, f, p, ZZ)
            g = gf_sub_ground(g, 1, p, ZZ)
            g = gf_gcd(f, g, p, ZZ)
            if 1 < len(g) < len(f):
                factors.append(g)
                factors.append(gf_div(f, g, p, ZZ)[0])
                break
    return sorted(root)

