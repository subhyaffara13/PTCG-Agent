
def _kl_gamma_exponential(p, q):
    return -p.entropy() - q.rate.log() + q.rate * p.concentration / p.rate

