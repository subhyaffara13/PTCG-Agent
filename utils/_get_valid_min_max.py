
def _get_valid_min_max(qparams):
    scale, zero_point, _quantized_type = qparams
    adjustment = 1 + torch.finfo(torch.float).eps
    _long_type_info = torch.iinfo(torch.long)
    long_min, long_max = _long_type_info.min / adjustment, _long_type_info.max / adjustment
    # make sure intermediate results are within the range of long
    min_value = max((long_min - zero_point) * scale, (long_min / scale + zero_point))
    max_value = min((long_max - zero_point) * scale, (long_max / scale + zero_point))
    return np.float32(min_value), np.float32(max_value)

