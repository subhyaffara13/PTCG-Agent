import math


def burr12_pdf(x, cc, dd):
    if x > 0:
        lx = math.log(x)
        logterm = math.log1p(math.exp(cc * lx))
        return math.exp((cc - 1) * lx - (dd + 1) * logterm + math.log(cc * dd))
    else:
        return 0

