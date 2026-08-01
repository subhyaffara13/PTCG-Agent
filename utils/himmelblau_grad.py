
def himmelblau_grad(p):
    x, y = p
    return np.array([4*x**3 + 4*x*y - 42*x + 2*y**2 - 14,
                     2*x**2 + 4*x*y + 4*y**3 - 26*y - 22])

