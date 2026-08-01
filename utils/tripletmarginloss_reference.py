
def tripletmarginloss_reference(anchor, positive, negative, margin=1.0, p=2, eps=1e-6, swap=False,
                                reduction='mean'):
    d_p = torch.pairwise_distance(anchor, positive, p, eps)
    d_n = torch.pairwise_distance(anchor, negative, p, eps)
    if swap:
        d_s = torch.pairwise_distance(positive, negative, p, eps)
        d_n = torch.min(d_n, d_s)

    output = torch.clamp(margin + d_p - d_n, min=0.0)
    if reduction == 'mean':
        return output.mean()
    elif reduction == 'sum':
        return output.sum()
    return output

