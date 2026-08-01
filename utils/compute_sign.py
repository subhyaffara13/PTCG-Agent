
def compute_sign(base, expo):
    '''
    base != 0 and expo >= 0 are integers;

    returns the sign of base**expo without
    evaluating the power itself!
    '''
    sb = sign(base)
    if sb == 1:
        return 1
    pe = expo % 2
    if pe == 0:
        return -sb
    else:
        return sb

