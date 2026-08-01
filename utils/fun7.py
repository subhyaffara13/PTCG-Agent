
def fun7(x):
    xp = array_namespace(x)
    return 0 if xp.abs(x) < 3.8e-4 else x*xp.exp(-x**(-2))

