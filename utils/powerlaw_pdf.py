
def powerlaw_pdf(x, a):
    if x > 0:
        return x ** (a - 1)
    return 0.0

