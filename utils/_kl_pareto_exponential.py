
def _kl_pareto_exponential(p, q):
    scale_rate_prod = p.scale * q.rate
    t1 = (p.alpha / scale_rate_prod).log()
    t2 = p.alpha.reciprocal()
    t3 = p.alpha * scale_rate_prod / (p.alpha - 1)
    result = t1 - t2 + t3 - 1
    result[p.alpha <= 1] = inf
    return result

