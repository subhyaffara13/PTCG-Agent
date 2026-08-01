
def _conv_corr_impl(a, v, mode):
    dt = _dtypes_impl.result_type_impl(a, v)
    a = _util.cast_if_needed(a, dt)
    v = _util.cast_if_needed(v, dt)

    padding = v.shape[0] - 1 if mode == "full" else mode

    if padding == "same" and v.shape[0] % 2 == 0:
        # UserWarning: Using padding='same' with even kernel lengths and odd
        # dilation may require a zero-padded copy of the input be created
        # (Triggered internally at pytorch/aten/src/ATen/native/Convolution.cpp:1010.)
        raise NotImplementedError("mode='same' and even-length weights")

    # NumPy only accepts 1D arrays; PyTorch requires 2D inputs and 3D weights
    aa = a[None, :]
    vv = v[None, None, :]

    result = torch.nn.functional.conv1d(aa, vv, padding=padding)

    # torch returns a 2D result, numpy returns a 1D array
    return result[0, :]

