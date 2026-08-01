
def _kl_dirichlet_dirichlet(p, q):
    # From http://bariskurt.com/kullback-leibler-divergence-between-two-dirichlet-and-beta-distributions/
    sum_p_concentration = p.concentration.sum(-1)
    sum_q_concentration = q.concentration.sum(-1)
    t1 = sum_p_concentration.lgamma() - sum_q_concentration.lgamma()
    t2 = (p.concentration.lgamma() - q.concentration.lgamma()).sum(-1)
    t3 = p.concentration - q.concentration
    t4 = p.concentration.digamma() - sum_p_concentration.digamma().unsqueeze(-1)
    return t1 - t2 + (t3 * t4).sum(-1)

