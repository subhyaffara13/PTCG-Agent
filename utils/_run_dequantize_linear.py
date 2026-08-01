
def _run_dequantize_linear(
    weight_tensor: numpy.ndarray, weight_scale: numpy.ndarray, weight_zp: numpy.ndarray, channel_axis: int
) -> numpy.ndarray | None:
    assert weight_scale.shape == weight_zp.shape
    if weight_zp.size == 1:
        return (weight_tensor - weight_zp) * weight_scale

    assert weight_zp.ndim == 1
    reshape_dims = list(weight_tensor.shape)  # deep copy
    reshape_dims[channel_axis] = 1  # only one per channel for reshape
    channel_count = weight_tensor.shape[channel_axis]
    dequantized_weights = None
    for i in range(channel_count):
        per_channel_data = weight_tensor.take(i, channel_axis)
        dequantized_per_channel_data = (per_channel_data - weight_zp[i]) * weight_scale[i]
        if i == 0:
            dequantized_weights = numpy.asarray(dequantized_per_channel_data).reshape(reshape_dims)
        else:
            channel_weights = numpy.asarray(dequantized_per_channel_data).reshape(reshape_dims)
            dequantized_weights = numpy.concatenate((dequantized_weights, channel_weights), channel_axis)

    if dequantized_weights is None:
        return None

    dequantized_weights.reshape(weight_tensor.shape)
    return dequantized_weights

