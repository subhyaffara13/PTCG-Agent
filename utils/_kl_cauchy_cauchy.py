
def _kl_cauchy_cauchy(p, q):
    # From https://arxiv.org/abs/1905.10965
    t1 = ((p.scale + q.scale).pow(2) + (p.loc - q.loc).pow(2)).log()
    t2 = (4 * p.scale * q.scale).log()
    return t1 - t2

