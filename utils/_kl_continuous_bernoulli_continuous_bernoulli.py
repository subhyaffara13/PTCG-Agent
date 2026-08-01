
def _kl_continuous_bernoulli_continuous_bernoulli(p, q):
    t1 = p.mean * (p.logits - q.logits)
    t2 = p._cont_bern_log_norm() + torch.log1p(-p.probs)
    t3 = -q._cont_bern_log_norm() - torch.log1p(-q.probs)
    return t1 + t2 + t3

