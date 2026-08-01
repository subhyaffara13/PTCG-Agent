
def reference_smooth_l1_loss(input, target, beta=1.0):
    diff = input - target
    abs_diff = np.abs(diff)
    above_threshold = abs_diff >= beta

    loss = np.empty_like(input)
    loss[above_threshold] = abs_diff[above_threshold] - 0.5 * beta
    loss[~above_threshold] = diff[~above_threshold] ** 2 / (2 * beta)

    return loss

