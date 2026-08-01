
def per_channel_tensor(draw, shapes=None, elements=None, qparams=None):
    if isinstance(shapes, SearchStrategy):
        _shape = draw(shapes)
    else:
        _shape = draw(st.sampled_from(shapes))
    if qparams is None:
        if elements is None:
            elements = floats(-1e6, 1e6, allow_nan=False, width=32)
        X = draw(stnp.arrays(dtype=np.float32, elements=elements, shape=_shape))
        assume(not (np.isnan(X).any() or np.isinf(X).any()))
        return X, None
    qparams = draw(qparams)
    if elements is None:
        min_value, max_value = _get_valid_min_max(qparams)
        elements = floats(min_value, max_value, allow_infinity=False,
                          allow_nan=False, width=32)
    X = draw(stnp.arrays(dtype=np.float32, elements=elements, shape=_shape))
    # Recompute the scale and zero_points according to the X statistics.
    scale, zp = _calculate_dynamic_per_channel_qparams(X, qparams[2])
    enforced_zp = _ENFORCED_ZERO_POINT.get(qparams[2], None)
    if enforced_zp is not None:
        zp = enforced_zp
    # Permute to model quantization along an axis
    axis = int(np.random.randint(0, X.ndim, 1))
    permute_axes = np.arange(X.ndim)
    permute_axes[0] = axis
    permute_axes[axis] = 0
    X = np.transpose(X, permute_axes)

    return X, (scale, zp, axis, qparams[2])

