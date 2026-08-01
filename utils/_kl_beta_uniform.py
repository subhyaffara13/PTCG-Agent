
def _kl_beta_uniform(p, q):
    result = -p.entropy() + (q.high - q.low).log()
    result[(q.low > p.support.lower_bound) | (q.high < p.support.upper_bound)] = inf
    return result

