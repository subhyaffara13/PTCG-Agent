
def egypt_golomb(x, y):
    # assumes x < y and gcd(x, y) == 1
    if x == 1:
        return [y]
    xp = sympy.polys.ZZ.invert(int(x), int(y))
    rv = [xp*y]
    rv.extend(egypt_golomb((x*xp - 1)//y, xp))
    return sorted(rv)

