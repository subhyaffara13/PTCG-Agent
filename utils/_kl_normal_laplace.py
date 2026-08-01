
def _kl_normal_laplace(p, q):
    loc_diff = p.loc - q.loc
    scale_ratio = p.scale / q.scale
    loc_diff_scale_ratio = loc_diff / p.scale
    t1 = torch.log(scale_ratio)
    t2 = (
        math.sqrt(2 / math.pi) * p.scale * torch.exp(-0.5 * loc_diff_scale_ratio.pow(2))
    )
    t3 = loc_diff * torch.erf(math.sqrt(0.5) * loc_diff_scale_ratio)
    return -t1 + (t2 + t3) / q.scale - (0.5 * (1 + math.log(0.5 * math.pi)))

