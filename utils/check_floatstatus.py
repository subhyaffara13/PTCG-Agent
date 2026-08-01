
def check_floatstatus(divbyzero=False, overflow=False,
                      underflow=False, invalid=False,
                      all=False):
    #define NPY_FPE_DIVIDEBYZERO  1
    #define NPY_FPE_OVERFLOW      2
    #define NPY_FPE_UNDERFLOW     4
    #define NPY_FPE_INVALID       8
    err = get_floatstatus()
    ret = (all or divbyzero) and (err & 1) != 0
    ret |= (all or overflow) and (err & 2) != 0
    ret |= (all or underflow) and (err & 4) != 0
    ret |= (all or invalid) and (err & 8) != 0
    return ret

