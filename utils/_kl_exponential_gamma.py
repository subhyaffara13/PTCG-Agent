
def _kl_exponential_gamma(p, q):
    ratio = q.rate / p.rate
    t1 = -q.concentration * torch.log(ratio)
    return (
        t1
        + ratio
        + q.concentration.lgamma()
        + q.concentration * _euler_gamma
        - (1 + _euler_gamma)
    )

