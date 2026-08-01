
def _rebuild_qtensor(
    storage,
    storage_offset,
    size,
    stride,
    quantizer_params,
    requires_grad,
    backward_hooks,
):
    qscheme = quantizer_params[0]
    if qscheme == torch.per_tensor_affine:
        _, scale, zero_point = quantizer_params
        tensor = torch._empty_affine_quantized(
            size,
            scale=scale,
            zero_point=zero_point,
            dtype=storage.dtype,
            device=storage.device,
        )
    elif qscheme in (torch.per_channel_affine, torch.per_channel_affine_float_qparams):
        _, scales, zero_points, axis = quantizer_params
        if type(scales) is list and type(zero_points) is list:
            if qscheme == torch.per_channel_affine:
                scales = torch.tensor(scales, dtype=torch.double, device=storage.device)
                zero_points = torch.tensor(
                    zero_points, dtype=torch.long, device=storage.device
                )
            else:
                scales = torch.tensor(scales, dtype=torch.float, device=storage.device)
                zero_points = torch.tensor(
                    zero_points, dtype=torch.float, device=storage.device
                )
        tensor = torch._empty_per_channel_affine_quantized(
            size,
            scales=scales,
            zero_points=zero_points,
            axis=axis,
            dtype=storage.dtype,
            device=storage.device,
        )
    else:
        raise RuntimeError(f"Can't deserialize quantized tensor with qscheme {qscheme}")
    tensor.set_(storage, storage_offset, size, stride)
    tensor.requires_grad = requires_grad
    # NB: This line exists only for backwards compatibility; the
    # general expectation is that backward_hooks is an empty
    # OrderedDict.  See Note [Don't serialize hooks]
    tensor._backward_hooks = backward_hooks
    return tensor

