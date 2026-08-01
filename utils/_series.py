
def _series(j, n, prec=14):

    # Left sum from the bbp algorithm
    s = 0
    D = _dn(n, prec)
    D4 = 4 * D
    d = j
    for k in range(n + 1):
        s += (pow(16, n - k, d) << D4) // d
        d += 8

    # Right sum iterates to infinity for full precision, but we
    # stop at the point where one iteration is beyond the precision
    # specified.

    t = 0
    k = n + 1
    e = D4 - 4 # 4*(D + n - k)
    d = 8 * k + j
    while True:
        dt = (1 << e) // d
        if not dt:
            break
        t += dt
        # k += 1
        e -= 4
        d += 8
    total = s + t

    return total

