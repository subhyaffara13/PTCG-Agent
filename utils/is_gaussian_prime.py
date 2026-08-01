
def is_gaussian_prime(num):
    r"""Test if num is a Gaussian prime number.

    References
    ==========

    .. [1] https://oeis.org/wiki/Gaussian_primes
    """

    num = sympify(num)
    a, b = num.as_real_imag()
    a = as_int(a, strict=False)
    b = as_int(b, strict=False)
    if a == 0:
        b = abs(b)
        return isprime(b) and b % 4 == 3
    elif b == 0:
        a = abs(a)
        return isprime(a) and a % 4 == 3
    return isprime(a**2 + b**2)

