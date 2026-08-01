
def assume_not_overflowing(tensor, qparams):
    min_value, max_value = _get_valid_min_max(qparams)
    assume(tensor.min() >= min_value)
    assume(tensor.max() <= max_value)
    return True

