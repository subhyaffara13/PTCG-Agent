
def _kl_uniform_continuous_bernoulli(p, q):
    result = (
        -p.entropy()
        - p.mean * q.logits
        - torch.log1p(-q.probs)
        - q._cont_bern_log_norm()
    )
    return torch.where(
        torch.max(
            torch.ge(p.high, q.support.upper_bound),
            torch.le(p.low, q.support.lower_bound),
        ),
        torch.ones_like(result) * inf,
        result,
    )

