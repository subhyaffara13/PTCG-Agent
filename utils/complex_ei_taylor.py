
def complex_ei_taylor(zre, zim, prec):
    _abs = abs
    sre = tre = zre
    sim = tim = zim
    k = 2
    while _abs(tre) + _abs(tim) > 5:
        tre, tim = ((tre*zre-tim*zim)//k)>>prec, ((tre*zim+tim*zre)//k)>>prec
        sre += tre // k
        sim += tim // k
        k += 1
    return sre, sim

