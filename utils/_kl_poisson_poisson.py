
def _kl_poisson_poisson(p, q):
    return p.rate * (p.rate.log() - q.rate.log()) - (p.rate - q.rate)

