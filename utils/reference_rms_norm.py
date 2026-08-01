
def reference_rms_norm(inp: npt.NDArray, normalized_shape: tuple[int, ...], weight=None, eps=None):
    if eps is None:
        eps = torch.finfo(numpy_to_torch_dtype(inp.dtype)).eps
    feature_size = np.prod(normalized_shape)
    inp_view = inp.reshape(-1, feature_size)  # type: ignore[call-overload]
    rms = np.sqrt((inp_view**2).mean(axis=-1, keepdims=True) + eps)
    Y = inp_view / rms
    if weight is not None:
        Y = Y * weight.reshape(-1)
    return Y.reshape(*inp.shape)

