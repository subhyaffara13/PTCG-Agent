
def rsa_crt_dmq1(private_exponent: int, q: int) -> int:
    """
    Compute the CRT private_exponent % (q - 1) value from the RSA
    private_exponent (d) and q.
    """
    if private_exponent <= 1 or q <= 1:
        raise ValueError("Values can't be <= 1")
    return private_exponent % (q - 1)

