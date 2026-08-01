
def convert_add(add):
    if add.ADD():
        lh = convert_add(add.additive(0))
        rh = convert_add(add.additive(1))
        return sympy.Add(lh, rh, evaluate=False)
    elif add.SUB():
        lh = convert_add(add.additive(0))
        rh = convert_add(add.additive(1))
        if hasattr(rh, "is_Atom") and rh.is_Atom:
            return sympy.Add(lh, -1 * rh, evaluate=False)
        return sympy.Add(lh, sympy.Mul(-1, rh, evaluate=False), evaluate=False)
    else:
        return convert_mp(add.mp())

