
def _kl_geometric_geometric(p, q):
    return -p.entropy() - torch.log1p(-q.probs) / p.probs - q.logits

