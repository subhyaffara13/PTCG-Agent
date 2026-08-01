
def _kl_pareto_gamma(p, q):
    common_term = p.scale.log() + p.alpha.reciprocal()
    t1 = p.alpha.log() - common_term
    t2 = q.concentration.lgamma() - q.concentration * q.rate.log()
    t3 = (1 - q.concentration) * common_term
    t4 = q.rate * p.alpha * p.scale / (p.alpha - 1)
    result = t1 + t2 + t3 + t4 - 1
    result[p.alpha <= 1] = inf
    return result

