
def _kl_uniform_gamma(p, q):
    common_term = p.high - p.low
    t1 = common_term.log()
    t2 = q.concentration.lgamma() - q.concentration * q.rate.log()
    t3 = (
        (1 - q.concentration)
        * (_x_log_x(p.high) - _x_log_x(p.low) - common_term)
        / common_term
    )
    t4 = q.rate * (p.high + p.low) / 2
    result = -t1 + t2 + t3 + t4
    result[p.low < q.support.lower_bound] = inf
    return result

