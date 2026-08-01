
def _freq_weights(weights):
    if weights is None:
        return weights
    int_weights = weights.astype(int)
    if (weights != int_weights).any():
        raise ValueError(f"frequency (integer count-type) weights required {weights}")
    return int_weights

