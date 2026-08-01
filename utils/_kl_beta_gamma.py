
def _kl_beta_gamma(p, q):
    t1 = -p.entropy()
    t2 = q.concentration.lgamma() - q.concentration * q.rate.log()
    t3 = (q.concentration - 1) * (
        p.concentration1.digamma() - (p.concentration1 + p.concentration0).digamma()
    )
    t4 = q.rate * p.concentration1 / (p.concentration1 + p.concentration0)
    return t1 + t2 - t3 + t4

