import random

def rsa_recover_prime_factors(n: int, e: int, d: int) -> tuple[int, int]:
    """
    Compute factors p and q from the private exponent d. We assume that n has
    no more than two factors. This function is adapted from code in PyCrypto.
    """
    # reject invalid values early
    if d <= 1 or e <= 1:
        raise ValueError("d, e can't be <= 1")
    if 17 != pow(17, e * d, n):
        raise ValueError("n, d, e don't match")
    # See 8.2.2(i) in Handbook of Applied Cryptography.
    ktot = d * e - 1
    # The quantity d*e-1 is a multiple of phi(n), even,
    # and can be represented as t*2^s.
    t = ktot
    while t % 2 == 0:
        t = t // 2
    # Cycle through all multiplicative inverses in Zn.
    # The algorithm is non-deterministic, but there is a 50% chance
    # any candidate a leads to successful factoring.
    # See "Digitalized Signatures and Public Key Functions as Intractable
    # as Factorization", M. Rabin, 1979
    spotted = False
    tries = 0
    while not spotted and tries < _MAX_RECOVERY_ATTEMPTS:
        a = random.randint(2, n - 1)
        tries += 1
        k = t
        # Cycle through all values a^{t*2^i}=a^k
        while k < ktot:
            cand = pow(a, k, n)
            # Check if a^k is a non-trivial root of unity (mod n)
            if cand != 1 and cand != (n - 1) and pow(cand, 2, n) == 1:
                # We have found a number such that (cand-1)(cand+1)=0 (mod n).
                # Either of the terms divides n.
                p = gcd(cand + 1, n)
                spotted = True
                break
            k *= 2
    if not spotted:
        raise ValueError("Unable to compute factors p and q from exponent d.")
    # Found !
    q, r = divmod(n, p)
    assert r == 0
    p, q = sorted((p, q), reverse=True)
    return (p, q)

