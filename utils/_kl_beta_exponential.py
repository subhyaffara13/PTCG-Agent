
def _kl_beta_exponential(p, q):
    return (
        -p.entropy()
        - q.rate.log()
        + q.rate * (p.concentration1 / (p.concentration1 + p.concentration0))
    )

