
def mpc_harmonic(z, prec, rnd):
    if z[1] == fzero:
        return (mpf_harmonic(z[0], prec, rnd), fzero)
    a = mpc_psi0(mpc_add_mpf(z, fone, prec+5), prec)
    return mpc_add_mpf(a, mpf_euler(prec+5, rnd), prec, rnd)

