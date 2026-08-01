
def get_elsize(var):
    if isstring(var) or isstringarray(var):
        elsize = getstrlength(var)
        # override with user-specified length when available:
        elsize = var['charselector'].get('f2py_len', elsize)
        return elsize
    if ischaracter(var) or ischaracterarray(var):
        return '1'
    # for numerical types, PyArray_New* functions ignore specified
    # elsize, so we just return 1 and let elsize be determined at
    # runtime, see fortranobject.c
    return '1'

