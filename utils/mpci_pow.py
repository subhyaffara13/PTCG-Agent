
def mpci_pow(x, y, prec):
    # TODO: recognize/speed up real cases, integer y
    yre, yim = y
    if yim == mpi_zero:
        ya, yb = yre
        if ya == yb:
            sign, man, exp, bc = yb
            if man and exp >= 0:
                return mpci_pow_int(x, (-1)**sign * int(man<<exp), prec)
            # x^0
            if yb == fzero:
                return mpci_pow_int(x, 0, prec)
    wp = prec+20
    return mpci_exp(mpci_mul(y, mpci_log(x, wp), wp), prec)

