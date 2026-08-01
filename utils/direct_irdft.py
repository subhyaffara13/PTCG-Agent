
def direct_irdft(x):
    x = asarray(x)
    n = len(x)
    x1 = zeros(n, dtype=cdouble)
    for i in range(n//2+1):
        if i:
            if 2*i < n:
                x1[i] = x[2*i-1] + 1j*x[2*i]
                x1[n-i] = x[2*i-1] - 1j*x[2*i]
            else:
                x1[i] = x[2*i-1]
        else:
            x1[0] = x[0]
    return direct_idft(x1).real


def direct_irdft(x, n):
    x = asarray(x)
    x1 = zeros(n, dtype=cdouble)
    for i in range(n//2+1):
        x1[i] = x[i]
        if i > 0 and 2*i < n:
            x1[n-i] = np.conj(x[i])
    return direct_idft(x1).real

