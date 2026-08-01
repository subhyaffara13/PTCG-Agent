
def is_fermat_prp(n, a):
    if a < 2:
        raise ValueError("is_fermat_prp() requires 'a' greater than or equal to 2")
    if n < 1:
        raise ValueError("is_fermat_prp() requires 'n' be greater than 0")
    if n == 1:
        return False
    if n % 2 == 0:
        return n == 2
    a %= n
    if gcd(n, a) != 1:
        raise ValueError("is_fermat_prp() requires gcd(n,a) == 1")
    return pow(a, n - 1, n) == 1

