
def naive_dst4(x, norm=None):
    """Calculate textbook definition version of DST-IV."""
    x = np.array(x, copy=True)
    N = len(x)
    y = np.zeros(N)
    for k in range(N):
        for n in range(N):
            y[k] += x[n]*np.sin(np.pi*(n+0.5)*(k+0.5)/(N))
    if norm == 'ortho':
        y *= np.sqrt(2.0/N)
    else:
        y *= 2
    return y


def naive_dst4(x, norm=None):
    """Calculate textbook definition version of DST-IV."""
    x = np.array(x, copy=True)
    N = len(x)
    y = np.zeros(N)
    for k in range(N):
        for n in range(N):
            y[k] += x[n]*np.sin(np.pi*(n+0.5)*(k+0.5)/(N))
    if norm == 'ortho':
        y *= np.sqrt(2.0/N)
    else:
        y *= 2
    return y

