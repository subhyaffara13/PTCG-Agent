
def _kl_uniform_pareto(p, q):
    support_uniform = p.high - p.low
    t1 = (q.alpha * q.scale.pow(q.alpha) * (support_uniform)).log()
    t2 = (_x_log_x(p.high) - _x_log_x(p.low) - support_uniform) / support_uniform
    result = t2 * (q.alpha + 1) - t1
    result[p.low < q.support.lower_bound] = inf
    return result

