
def mpi_div(s, t, prec):
    sa, sb = s
    ta, tb = t
    sas = mpf_sign(sa)
    sbs = mpf_sign(sb)
    tas = mpf_sign(ta)
    tbs = mpf_sign(tb)
    # 0 / X
    if sas == sbs == 0:
        # 0 / <interval containing 0>
        if (tas < 0 and tbs > 0) or (tas == 0 or tbs == 0):
            return fninf, finf
        return fzero, fzero
    # Denominator contains both negative and positive numbers;
    # this should properly be a multi-interval, but the closest
    # match is the entire (extended) real line
    if tas < 0 and tbs > 0:
        return fninf, finf
    # Assume denominator to be nonnegative
    if tas < 0:
        return mpi_div(mpi_neg(s), mpi_neg(t), prec)
    # Division by zero
    # XXX: make sure all results make sense
    if tas == 0:
        # Numerator contains both signs?
        if sas < 0 and sbs > 0:
            return fninf, finf
        if tas == tbs:
            return fninf, finf
        # Numerator positive?
        if sas >= 0:
            a = mpf_div(sa, tb, prec, round_floor)
            b = finf
        if sbs <= 0:
            a = fninf
            b = mpf_div(sb, tb, prec, round_ceiling)
    # Division with positive denominator
    # We still have to handle nans resulting from inf/0 or inf/inf
    else:
        # Nonnegative numerator
        if sas >= 0:
            a = mpf_div(sa, tb, prec, round_floor)
            b = mpf_div(sb, ta, prec, round_ceiling)
            if a == fnan: a = fzero
            if b == fnan: b = finf
        # Nonpositive numerator
        elif sbs <= 0:
            a = mpf_div(sa, ta, prec, round_floor)
            b = mpf_div(sb, tb, prec, round_ceiling)
            if a == fnan: a = fninf
            if b == fnan: b = fzero
        # Numerator contains both signs?
        else:
            a = mpf_div(sa, ta, prec, round_floor)
            b = mpf_div(sb, ta, prec, round_ceiling)
            if a == fnan: a = fninf
            if b == fnan: b = finf
    return a, b

