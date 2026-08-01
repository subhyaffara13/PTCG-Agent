
def rsa_crt_iqmp(p: int, q: int) -> int:
    """
    Compute the CRT (q ** -1) % p value from RSA primes p and q.
    """
    if p <= 1 or q <= 1:
        raise ValueError("Values can't be <= 1")
    return _modinv(q, p)

