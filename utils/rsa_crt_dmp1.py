
def rsa_crt_dmp1(private_exponent: int, p: int) -> int:
    """
    Compute the CRT private_exponent % (p - 1) value from the RSA
    private_exponent (d) and p.
    """
    if private_exponent <= 1 or p <= 1:
        raise ValueError("Values can't be <= 1")
    return private_exponent % (p - 1)

