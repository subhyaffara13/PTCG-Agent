
def _kl_gamma_normal(p, q):
    var_normal = q.scale.pow(2)
    beta_sqr = p.rate.pow(2)
    t1 = (
        0.5 * torch.log(beta_sqr * var_normal * 2 * math.pi)
        - p.concentration
        - p.concentration.lgamma()
    )
    t2 = 0.5 * (p.concentration.pow(2) + p.concentration) / beta_sqr
    t3 = q.loc * p.concentration / p.rate
    t4 = 0.5 * q.loc.pow(2)
    return (
        t1
        + (p.concentration - 1) * p.concentration.digamma()
        + (t2 - t3 + t4) / var_normal
    )

