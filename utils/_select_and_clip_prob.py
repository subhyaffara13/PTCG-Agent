
def _select_and_clip_prob(cdfprob, sfprob, cdf=True):
    """Selects either the CDF or SF, and then clips to range 0<=p<=1."""
    p = np.where(cdf, cdfprob, sfprob)
    return _clip_prob(p)

