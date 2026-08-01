
def complex_ei_asymptotic(zre, zim, prec):
    _abs = abs
    one = MPZ_ONE << prec
    M = (zim*zim + zre*zre) >> prec
    # 1 / z
    xre = tre = (zre << prec) // M
    xim = tim = ((-zim) << prec) // M
    sre = one + xre
    sim = xim
    k = 2
    while _abs(tre) + _abs(tim) > 1000:
        #print tre, tim
        tre, tim = ((tre*xre-tim*xim)*k)>>prec, ((tre*xim+tim*xre)*k)>>prec
        sre += tre
        sim += tim
        k += 1
        if k > prec:
            raise NoConvergence
    return sre, sim

