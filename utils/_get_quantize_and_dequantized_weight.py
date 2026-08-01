
def _get_quantize_and_dequantized_weight(module, wn):
    if not hasattr(module, wn):
        return None
    params = _get_weight_and_quantization_params(module, wn)
    weight = _quantize_and_dequantize_weight(*params)
    return weight

