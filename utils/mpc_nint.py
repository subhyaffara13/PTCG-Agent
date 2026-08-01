
def mpc_nint(z, prec, rnd=round_fast):
    a, b = z
    return mpf_nint(a, prec, rnd), mpf_nint(b, prec, rnd)

