
def isarrayofstrings(var):  # obsolete?
    # leaving out '*' for now so that `character*(*) a(m)` and `character
    # a(m,*)` are treated differently. Luckily `character**` is illegal.
    return isstringarray(var) and var['dimension'][-1] == '(*)'

