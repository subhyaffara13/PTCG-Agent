
def _kl_gamma_gumbel(p, q):
    beta_scale_prod = p.rate * q.scale
    loc_scale_ratio = q.loc / q.scale
    t1 = (
        (p.concentration - 1) * p.concentration.digamma()
        - p.concentration.lgamma()
        - p.concentration
    )
    t2 = beta_scale_prod.log() + p.concentration / beta_scale_prod
    t3 = (
        torch.exp(loc_scale_ratio)
        * (1 + beta_scale_prod.reciprocal()).pow(-p.concentration)
        - loc_scale_ratio
    )
    return t1 + t2 + t3

