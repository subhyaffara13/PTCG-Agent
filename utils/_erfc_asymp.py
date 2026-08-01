
def _erfc_asymp(x):
    # Asymptotic expansion assuming x >= 9
    x2 = x*x
    v = exp(-x2)/x*0.56418958354775628695
    r = t = 0.5 / x2
    s = 1.0
    for n in range(1,22,4):
        s -= t
        t *= r * (n+2)
        s += t
        t *= r * (n+4)
        if abs(t) < 1e-17:
            break
    return s * v

