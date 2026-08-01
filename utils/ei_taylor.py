
def ei_taylor(z, _e1=False):
    s = t = z
    k = 2
    while 1:
        t = t*z/k
        term = t/k
        if abs(term) < 1e-17:
            break
        s += term
        k += 1
    s += euler
    if _e1:
        s += log(-z)
    else:
        if type(z) is float or z.imag == 0.0:
            s += math_log(abs(z))
        else:
            s += cmath.log(z)
    return s


def ei_taylor(x, prec):
    s = t = x
    k = 2
    while t:
        t = ((t*x) >> prec) // k
        s += t // k
        k += 1
    return s

