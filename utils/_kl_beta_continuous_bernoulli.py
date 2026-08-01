
def _kl_beta_continuous_bernoulli(p, q):
    return (
        -p.entropy()
        - p.mean * q.logits
        - torch.log1p(-q.probs)
        - q._cont_bern_log_norm()
    )

