
def _kl_uniform_exponetial(p, q):
    result = q.rate * (p.high + p.low) / 2 - ((p.high - p.low) * q.rate).log()
    result[p.low < q.support.lower_bound] = inf
    return result

