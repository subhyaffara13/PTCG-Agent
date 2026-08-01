
def _strong_probable_prime(n, base):
    assert (n > 2) and (n & 1) and (2 <= base < n)

    s, d = _shift_to_odd(n - 1)

    x = pow(base, d, n)
    if x == 1 or x == n - 1:
        return True

    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True

    return False

