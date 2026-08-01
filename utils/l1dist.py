
def l1dist(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))

