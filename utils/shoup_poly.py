
def shoup_poly(n, p, K):
    f = [K.one] * (n + 1)
    for i in range(1, n + 1):
        f[i] = (f[i - 1]**2 + K.one) % p
    return f

