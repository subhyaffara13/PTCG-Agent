
def is_fibonacci_prp(n, p, q):
    d = p**2 - 4*q
    if d == 0 or p <= 0 or q not in [1, -1]:
        raise ValueError("invalid values for p,q in is_fibonacci_prp()")
    if n < 1:
        raise ValueError("is_fibonacci_prp() requires 'n' be greater than 0")
    if n == 1:
        return False
    if n % 2 == 0:
        return n == 2
    return _lucas_sequence(n, p, q, n)[1] == p % n

