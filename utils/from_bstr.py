
def from_bstr(x):
    man, exp = str_to_man_exp(x, base=2)
    man = MPZ(man)
    sign = 0
    if man < 0:
        man = -man
        sign = 1
    bc = bitcount(man)
    return normalize(sign, man, exp, bc, bc, round_floor)

