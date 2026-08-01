
def ae(x, y, tol=1e-12):
    if x == y:
        return True
    return abs(x-y) <= tol*abs(y)


def ae(a, b):
    return abs(a-b) < 10**(-mp.dps+5)

