
def _alpha_tr(step, sd, delta):
    step_sd = step @ sd
    sd_sq = sd @ sd
    dist_tr_sq = delta**2.0 - step @ step
    temp = np.sqrt(max(step_sd**2.0 + sd_sq * dist_tr_sq, 0.0))
    if step_sd <= 0.0 and sd_sq > TINY * abs(temp - step_sd):
        alpha_tr = max((temp - step_sd) / sd_sq, 0.0)
    elif abs(temp + step_sd) > TINY * dist_tr_sq:
        alpha_tr = max(dist_tr_sq / (temp + step_sd), 0.0)
    else:
        raise ZeroDivisionError
    return alpha_tr

