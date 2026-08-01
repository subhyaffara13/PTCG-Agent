
def round_fixed(x, prec):
    return ((x + (1<<(prec-1))) >> prec) << prec

