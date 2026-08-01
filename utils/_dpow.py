
def _dpow(x, y, n):
    """
    d^n (x**y) / dx^n
    """
    if n < 0:
        raise ValueError("invalid derivative order")
    elif n > y:
        return 0
    else:
        return poch(y - n + 1, n) * x**(y - n)

