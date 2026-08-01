
def diop_simplify(eq):
    return _mexpand(powsimp(_mexpand(eq)))

