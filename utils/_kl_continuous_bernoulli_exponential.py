
def _kl_continuous_bernoulli_exponential(p, q):
    return -p.entropy() - torch.log(q.rate) + q.rate * p.mean

