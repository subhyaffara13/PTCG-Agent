
def aps14_f(x, n):
    r"""0 for negative x-values, trigonometric+linear for x positive"""
    if x <= 0:
        return -n / 20.0
    return n / 20.0 * (x / 1.5 + np.sin(x) - 1)

