
def _is_nthpow_residue_bign_prime_power(a, n, p, k):
    r"""
    Returns True if `x^n = a \pmod{p^k}` has solutions for `n > 2`.

    Parameters
    ==========

    a : positive integer
    n : integer, n > 2
    p : prime number
    k : positive integer

    """
    while a % p == 0:
        a %= pow(p, k)
        if not a:
            return True
        a, mu = remove(a, p)
        if mu % n:
            return False
        k -= mu
    if p != 2:
        f = p**(k - 1)*(p - 1) # f = totient(p**k)
        return pow(a, f // gcd(f, n), pow(p, k)) == 1
    if n & 1:
        return True
    c = min(bit_scan1(n) + 2, k)
    return a % pow(2, c) == 1

