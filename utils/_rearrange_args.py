
def _rearrange_args(l):
    """ this just moves the last arg to first position
     to enable expansion of args
     A,B,A ==> A**2,B
    """
    if len(l) == 1:
        return l

    x = list(l[-1:])
    x.extend(l[0:-1])
    return Mul(*x).args

