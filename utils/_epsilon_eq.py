
def _epsilon_eq(a, b):
    for u, v in zip(a, b):
        if abs(u - v) > 1e-10:
            return False
    return True

