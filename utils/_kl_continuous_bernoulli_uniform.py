
def _kl_continuous_bernoulli_uniform(p, q):
    result = -p.entropy() + (q.high - q.low).log()
    return torch.where(
        torch.max(
            torch.ge(q.low, p.support.lower_bound),
            torch.le(q.high, p.support.upper_bound),
        ),
        torch.ones_like(result) * inf,
        result,
    )

