
def _is_strong_prp(n, a):
    s = bit_scan1(n - 1)
    a = pow(a, n >> s, n)
    if a == 1 or a == n - 1:
        return True
    for _ in range(s - 1):
        a = pow(a, 2, n)
        if a == n - 1:
            return True
        if a == 1:
            return False
    return False

