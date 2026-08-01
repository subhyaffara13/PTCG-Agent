
def bit_scan0(x, n=0):
    return bit_scan1(x + (1 << n), n)

