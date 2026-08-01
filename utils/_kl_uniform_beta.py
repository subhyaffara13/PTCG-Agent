
def _kl_uniform_beta(p, q):
    common_term = p.high - p.low
    t1 = torch.log(common_term)
    t2 = (
        (q.concentration1 - 1)
        * (_x_log_x(p.high) - _x_log_x(p.low) - common_term)
        / common_term
    )
    t3 = (
        (q.concentration0 - 1)
        * (_x_log_x(1 - p.high) - _x_log_x(1 - p.low) + common_term)
        / common_term
    )
    t4 = (
        q.concentration1.lgamma()
        + q.concentration0.lgamma()
        - (q.concentration1 + q.concentration0).lgamma()
    )
    result = t3 + t4 - t1 - t2
    result[(p.high > q.support.upper_bound) | (p.low < q.support.lower_bound)] = inf
    return result

