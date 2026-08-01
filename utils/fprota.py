
def fprota(c, s, a, b):
    """Givens rotate [a, b].

    [aa] = [ c s] @ [a]
    [bb]   [-s c]   [b]

    """
    aa =  c*a + s*b
    bb = -s*a + c*b
    return aa, bb

