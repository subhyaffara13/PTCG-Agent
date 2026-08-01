
def _shift_to_odd(n):
    'Return s, d such that 2**s * d == n'
    s = ((n - 1) ^ n).bit_length() - 1
    d = n >> s
    assert (1 << s) * d == n and d & 1 and s >= 0
    return s, d

