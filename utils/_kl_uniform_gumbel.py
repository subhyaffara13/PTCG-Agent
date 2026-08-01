
def _kl_uniform_gumbel(p, q):
    common_term = q.scale / (p.high - p.low)
    high_loc_diff = (p.high - q.loc) / q.scale
    low_loc_diff = (p.low - q.loc) / q.scale
    t1 = common_term.log() + 0.5 * (high_loc_diff + low_loc_diff)
    t2 = common_term * (torch.exp(-high_loc_diff) - torch.exp(-low_loc_diff))
    return t1 - t2

