
def direct_rdft(x):
    x = asarray(x)
    n = len(x)
    w = -arange(n)*(2j*pi/n)
    r = zeros(n, dtype=double)
    for i in range(n//2+1):
        y = dot(exp(i*w), x)
        if i:
            r[2*i-1] = y.real
            if 2*i < n:
                r[2*i] = y.imag
        else:
            r[0] = y.real
    return r


def direct_rdft(x):
    x = asarray(x)
    n = len(x)
    w = -arange(n)*(2j*pi/n)
    y = zeros(n//2+1, dtype=cdouble)
    for i in range(n//2+1):
        y[i] = dot(exp(i*w), x)
    return y

