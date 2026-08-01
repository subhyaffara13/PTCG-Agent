
def _kl_bernoulli_bernoulli(p, q):
    t1 = p.probs * (
        torch.nn.functional.softplus(-q.logits)
        - torch.nn.functional.softplus(-p.logits)
    )
    t1[q.probs == 0] = inf
    t1[p.probs == 0] = 0
    t2 = (1 - p.probs) * (
        torch.nn.functional.softplus(q.logits) - torch.nn.functional.softplus(p.logits)
    )
    t2[q.probs == 1] = inf
    t2[p.probs == 1] = 0
    return t1 + t2

