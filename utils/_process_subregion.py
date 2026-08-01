
def _process_subregion(data):
    f, rule, args, coord = data
    a_k_sub, b_k_sub = coord

    est_sub = rule.estimate(f, a_k_sub, b_k_sub, args)
    err_sub = rule.estimate_error(f, a_k_sub, b_k_sub, args)

    return a_k_sub, b_k_sub, est_sub, err_sub

