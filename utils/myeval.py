
def myeval(e, g=None, l=None):
    """ Like `eval` but returns only integers and floats """
    r = eval(e, g, l)
    if type(r) in [int, float]:
        return r
    raise ValueError(f'r={r!r}')

