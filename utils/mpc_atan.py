
def mpc_atan(z, prec, rnd=round_fast):
    a, b = z
    # atan(z) = (I/2)*(log(1-I*z) - log(1+I*z))
    # x = 1-I*z = 1 + b - I*a
    # y = 1+I*z = 1 - b + I*a
    wp = prec + 15
    x = mpf_add(fone, b, wp), mpf_neg(a)
    y = mpf_sub(fone, b, wp), a
    l1 = mpc_log(x, wp)
    l2 = mpc_log(y, wp)
    a, b = mpc_sub(l1, l2, prec, rnd)
    # (I/2) * (a+b*I) = (-b/2 + a/2*I)
    v = mpf_neg(mpf_shift(b,-1)), mpf_shift(a,-1)
    # Subtraction at infinity gives correct real part but
    # wrong imaginary part (should be zero)
    if v[1] == fnan and mpc_is_inf(z):
        v = (v[0], fzero)
    return v

