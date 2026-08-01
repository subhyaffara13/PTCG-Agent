
def euler_fixed(prec):
    extra = 30
    prec += extra
    # choose p such that exp(-4*(2**p)) < 2**-n
    p = int(math.log((prec/4) * math.log(2), 2)) + 1
    n = 2**p
    A = U = -p*ln2_fixed(prec)
    B = V = MPZ_ONE << prec
    k = 1
    while 1:
        B = B*n**2//k**2
        A = (A*n**2//k + B)//k
        U += A
        V += B
        if max(abs(A), abs(B)) < 100:
            break
        k += 1
    return (U<<(prec-extra))//V

