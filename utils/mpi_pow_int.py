
def mpi_pow_int(s, n, prec):
    sa, sb = s
    if n < 0:
        return mpi_div((fone, fone), mpi_pow_int(s, -n, prec+20), prec)
    if n == 0:
        return (fone, fone)
    if n == 1:
        return s
    if n == 2:
        return mpi_square(s, prec)
    # Odd -- signs are preserved
    if n & 1:
        a = mpf_pow_int(sa, n, prec, round_floor)
        b = mpf_pow_int(sb, n, prec, round_ceiling)
    # Even -- important to ensure positivity
    else:
        sas = mpf_sign(sa)
        sbs = mpf_sign(sb)
        # Nonnegative?
        if sas >= 0:
            a = mpf_pow_int(sa, n, prec, round_floor)
            b = mpf_pow_int(sb, n, prec, round_ceiling)
        # Nonpositive?
        elif sbs <= 0:
            a = mpf_pow_int(sb, n, prec, round_floor)
            b = mpf_pow_int(sa, n, prec, round_ceiling)
        # Mixed signs?
        else:
            a = fzero
            # max(-a,b)**n
            sa = mpf_neg(sa)
            if mpf_ge(sa, sb):
                b = mpf_pow_int(sa, n, prec, round_ceiling)
            else:
                b = mpf_pow_int(sb, n, prec, round_ceiling)
    return a, b

