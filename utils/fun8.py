
def fun8(x):
    xp = array_namespace(x)
    xi = 0.61489
    return -(3062*(1-xi)*xp.exp(-x))/(xi + (1-xi)*xp.exp(-x)) - 1013 + 1628/x

