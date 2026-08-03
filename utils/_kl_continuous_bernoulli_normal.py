import math


def _kl_continuous_bernoulli_normal(p, q):
    t1 = -p.entropy()
    t2 = 0.5 * (math.log(2.0 * math.pi) + torch.square(q.loc / q.scale)) + torch.log(
        q.scale
    )
    t3 = (p.variance + torch.square(p.mean) - 2.0 * q.loc * p.mean) / (
        2.0 * torch.square(q.scale)
    )
    return t1 + t2 + t3

