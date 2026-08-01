
def from_pickable(x):
    sign, man, exp, bc = x
    return (sign, MPZ(man, 16), exp, bc)

