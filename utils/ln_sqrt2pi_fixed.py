
def ln_sqrt2pi_fixed(prec):
    wp = prec + 10
    # ln(sqrt(2*pi)) = ln(2*pi)/2
    return to_fixed(mpf_log(mpf_shift(mpf_pi(wp), 1), wp), prec-1)

