
def _kl_binomial_binomial(p, q):
    # from https://math.stackexchange.com/questions/2214993/
    # kullback-leibler-divergence-for-binomial-distributions-p-and-q
    if (p.total_count < q.total_count).any():
        raise NotImplementedError(
            "KL between Binomials where q.total_count > p.total_count is not implemented"
        )
    kl = p.total_count * (
        p.probs * (p.logits - q.logits) + (-p.probs).log1p() - (-q.probs).log1p()
    )
    inf_idxs = p.total_count > q.total_count
    kl[inf_idxs] = _infinite_like(kl[inf_idxs])
    return kl

