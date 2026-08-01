
def _de_casteljau1(beta, t):
    next_beta = beta[:-1] * (1 - t) + beta[1:] * t
    return next_beta

