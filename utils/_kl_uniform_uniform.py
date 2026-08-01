
def _kl_uniform_uniform(p, q):
    result = ((q.high - q.low) / (p.high - p.low)).log()
    result[(q.low > p.low) | (q.high < p.high)] = inf
    return result

