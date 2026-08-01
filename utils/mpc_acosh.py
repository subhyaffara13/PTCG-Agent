
def mpc_acosh(z, prec, rnd=round_fast):
    # acosh(z) = -I * acos(z)   for Im(acos(z)) <= 0
    #            +I * acos(z)   otherwise
    a, b = mpc_acos(z, prec, rnd)
    if b[0] or b == fzero:
        return mpf_neg(b), a
    else:
        return b, mpf_neg(a)

