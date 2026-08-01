
def mpf_psi(m, x, prec, rnd=round_fast):
    """
    Computation of the polygamma function of arbitrary integer order
    m >= 0, for a real argument x.
    """
    if m == 0:
        return mpf_psi0(x, prec, rnd=round_fast)
    return mpc_psi(m, (x, fzero), prec, rnd)[0]

