
def _nthroot_mod_prime_power(a, n, p, k):
    """ Root of ``x**n = a mod p**k``.

    Parameters
    ==========

    a : integer
    n : integer, n > 2
    p : prime number
    k : positive integer

    Returns
    =======

    list[int] :
        Ascending list of roots of ``x**n = a mod p**k``.
        If no solution exists, return ``[]``.

    """
    if not _is_nthpow_residue_bign_prime_power(a, n, p, k):
        return []
    a_mod_p = a % p
    if a_mod_p == 0:
        base_roots = [0]
    elif (p - 1) % n == 0:
        base_roots = _nthroot_mod1(a_mod_p, n, p, all_roots=True)
    else:
        # The roots of ``x**n - a = 0 (mod p)`` are roots of
        # ``gcd(x**n - a, x**(p - 1) - 1) = 0 (mod p)``
        pa = n
        pb = p - 1
        b = 1
        if pa < pb:
            a_mod_p, pa, b, pb = b, pb, a_mod_p, pa
        # gcd(x**pa - a, x**pb - b) = gcd(x**pb - b, x**pc - c)
        # where pc = pa % pb; c = b**-q * a mod p
        while pb:
            q, pc = divmod(pa, pb)
            c = pow(b, -q, p) * a_mod_p % p
            pa, pb = pb, pc
            a_mod_p, b = b, c
        if pa == 1:
            base_roots = [a_mod_p]
        elif pa == 2:
            base_roots = sqrt_mod(a_mod_p, p, all_roots=True)
        else:
            base_roots = _nthroot_mod1(a_mod_p, pa, p, all_roots=True)
    if k == 1:
        return base_roots
    a %= p**k
    tot_roots = set()
    for root in base_roots:
        diff = pow(root, n - 1, p)*n % p
        new_base = p
        if diff != 0:
            m_inv = invert(diff, p)
            for _ in range(k - 1):
                new_base *= p
                tmp = pow(root, n, new_base) - a
                tmp *= m_inv
                root = (root - tmp) % new_base
            tot_roots.add(root)
        else:
            roots_in_base = {root}
            for _ in range(k - 1):
                new_base *= p
                new_roots = set()
                for k_ in roots_in_base:
                    if pow(k_, n, new_base) != a % new_base:
                        continue
                    while k_ not in new_roots:
                        new_roots.add(k_)
                        k_ = (k_ + (new_base // p)) % new_base
                roots_in_base = new_roots
            tot_roots = tot_roots | roots_in_base
    return sorted(tot_roots)

