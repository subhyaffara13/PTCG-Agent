
def _sfdp_pattern_28(query, key, value, scale_factor, dropout_p):
    # Visformer pattern
    # same as pattern 4 but non-contiguous q/k/v
    return _sfdp_pattern_4(query, key, value, scale_factor, dropout_p)

