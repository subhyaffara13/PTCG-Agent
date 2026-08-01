
def init_normal_DMF(num, den, lev, dom):
    return DMF(dmp_normal(num, lev, dom),
               dmp_normal(den, lev, dom), dom, lev)

