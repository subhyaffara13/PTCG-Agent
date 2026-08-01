
def huberloss_reference(input, target, reduction='mean', delta=1.0):
    abs_diff = (input - target).abs()
    ge_delta_mask = (abs_diff >= delta)
    lt_delta_mask = (abs_diff < delta)
    output = ge_delta_mask * delta * (abs_diff - 0.5 * delta) + lt_delta_mask * 0.5 * (abs_diff ** 2)
    if reduction == 'mean':
        return output.mean()
    elif reduction == 'sum':
        return output.sum()
    return output

