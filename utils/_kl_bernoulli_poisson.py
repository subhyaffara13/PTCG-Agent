
def _kl_bernoulli_poisson(p, q):
    return -p.entropy() - (p.probs * q.rate.log() - q.rate)

