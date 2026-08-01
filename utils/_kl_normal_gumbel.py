
def _kl_normal_gumbel(p, q):
    mean_scale_ratio = p.loc / q.scale
    var_scale_sqr_ratio = (p.scale / q.scale).pow(2)
    loc_scale_ratio = q.loc / q.scale
    t1 = var_scale_sqr_ratio.log() * 0.5
    t2 = mean_scale_ratio - loc_scale_ratio
    t3 = torch.exp(-mean_scale_ratio + 0.5 * var_scale_sqr_ratio + loc_scale_ratio)
    return -t1 + t2 + t3 - (0.5 * (1 + math.log(2 * math.pi)))

