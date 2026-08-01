
def quant_tensor_k_quant_cpu(data, num_bits=4, group_size=32):
    """Quantize tensor per group based on k quant.

    Ref: https://github.com/ggml-org/llama.cpp/blob/64eda5deb9859e87a020e56bab5d2f9ca956f1de/ggml/src/ggml-quants.c

    Args:
        data : input weight
        num_bits (int, optional): num_bits. Defaults to 4.
        group_size (int, optional): how many elements share one scale/zp. Defaults to 32.

    Returns:
        output: quantized weight
        scale: scale
        zero_point: zero point
    """
    data = np.reshape(data, (-1, group_size)).astype(np.float32)  # nb = data.shape[0], (nb, group_size)
    maxq = 2**num_bits - 1
    minq = 0
    sum_x2 = np.sum(data**2, axis=1, keepdims=True)  # (nb, 1)
    av_x = np.sqrt(sum_x2 / group_size)  # (nb, 1)
    weights = np.add(av_x, np.abs(data))  # (nb, group_size)
    rmin = np.min(data, axis=1, keepdims=True)  # (nb, 1)
    rmax = np.max(data, axis=1, keepdims=True)  # (nb, 1)
    sum_w = np.sum(weights, axis=1, keepdims=True)  # (nb, 1)
    sum_x = np.sum(weights * data, axis=1, keepdims=True)  # (nb, group_size)
    iscale = np.ones(rmax.shape, dtype=data.dtype)  # (nb, 1)
    mask = rmin != rmax
    iscale[mask] = (maxq - minq) / (rmax[mask] - rmin[mask])
    scale = 1 / iscale
    quant_data = np.clip(np.round(iscale * (data - rmin)), minq, maxq)  # (nb, group_size)
    diff = scale * quant_data + rmin - data  # (nb, group_size)
    best_mad = np.sum(weights * diff**2, axis=1, keepdims=True)  # (nb, 1)
    nstep = 20
    rdelta = 0.1
    # nstep * rdelta = -2 * rrmin, maxq - minq = 2**num_bits - 1
    rrmin = -1
    for is_ in range(nstep):
        iscale_new = np.ones(rmax.shape, dtype=data.dtype)  # (nb, 1)
        factor = np.array([rrmin + rdelta * is_ + maxq - minq]).astype(data.dtype)[0]
        mask = rmin != rmax
        iscale_new[mask] = factor / (rmax[mask] - rmin[mask])
        quant_data_new = np.clip(np.round(iscale_new * (data - rmin)), minq, maxq)  # (nb, group_size)
        mul_weights_quant_data_new = weights * quant_data_new
        sum_l = np.sum(mul_weights_quant_data_new, axis=1, keepdims=True)  # (nb, 1)
        sum_l2 = np.sum(mul_weights_quant_data_new * quant_data_new, axis=1, keepdims=True)  # (nb, 1)
        sum_xl = np.sum(mul_weights_quant_data_new * data, axis=1, keepdims=True)  # (nb, 1)
        D = np.subtract(sum_w * sum_l2, sum_l**2)  # noqa: N806

        this_scale = (sum_w * sum_xl - sum_x * sum_l) / D  # (nb, 1)
        this_min = (sum_l2 * sum_x - sum_l * sum_xl) / D  # (nb, 1)

        diff = this_scale * quant_data_new + this_min - data  # (nb, group_size)
        mad = np.sum(weights * diff**2, axis=1, keepdims=True)  # (nb, 1)

        mad_1 = np.array(mad)
        best_mad_1 = np.array(best_mad)
        idx_to_replace = np.where(mad_1 < best_mad_1)[0]
        quant_data[idx_to_replace, :] = quant_data_new[idx_to_replace, :]
        best_mad[idx_to_replace] = mad[idx_to_replace]
        scale[idx_to_replace] = this_scale[idx_to_replace]
        rmin[idx_to_replace] = this_min[idx_to_replace]

    zero_point = np.clip(((-rmin) / scale).round(), 0, maxq).astype("uint8")
    scale = scale.astype(np.float64)
    q_weight = np.empty_like(data, dtype=scale.dtype)
    np.divide(data, scale, out=q_weight)
    np.add(q_weight, zero_point, out=q_weight)
    np.round(q_weight, out=q_weight)
    np.clip(q_weight, minq, maxq, out=q_weight)

    return q_weight, scale, zero_point

