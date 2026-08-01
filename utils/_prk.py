
def _prk(r, k):
    # Writen to match [1] Equation 27 closely to facilitate review.
    # This does not protect against overflow, so improvements to
    # robustness would be a welcome follow-up.
    binom_r_k = xpx.lazy_apply(special.binom, r, k)
    binom_rpk_k = xpx.lazy_apply(special.binom, r+k, k)
    return (-1)**(r-k)*binom_r_k*binom_rpk_k

