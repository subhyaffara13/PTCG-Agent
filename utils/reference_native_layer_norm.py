
def reference_native_layer_norm(inp: npt.NDArray, normalized_shape: tuple[int, ...], weight, bias, eps):
    feature_size = np.prod(normalized_shape)
    inp_view = inp.reshape(-1, feature_size)  # type: ignore[call-overload]
    mean = inp_view.mean(axis=-1, keepdims=True)
    var = inp_view.var(axis=-1, ddof=0, keepdims=True)
    Y = (inp_view - mean) / np.sqrt(var + eps)
    if weight is None and bias is not None:
        Y = Y + bias.reshape(-1)
    elif weight is not None and bias is None:
        Y = Y * weight.reshape(-1)
    elif weight is not None and bias is not None:
        Y = Y * weight.reshape(-1) + bias.reshape(-1)
    axis = inp.ndim - len(normalized_shape)
    stat_shape = inp.shape[:axis] + (1,) * len(normalized_shape)
    return Y.reshape(*inp.shape), mean.reshape(stat_shape), (1.0 / np.sqrt(var + eps)).reshape(stat_shape)

