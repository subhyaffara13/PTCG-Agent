
def get_tensor_from_qtensor(
    qtensor: torch.Tensor, dequant: bool = True
) -> torch.Tensor:
    # Manual conversion because qint8 is not used anymore.
    if qtensor.dtype in [torch.qint8, torch.quint8]:
        tensor = qtensor.int_repr()
    else:
        tensor = qtensor

    # Weights need dequantization with scaling and zero_point adjustment, but
    # bias does not need that.
    if dequant:
        qscheme = qtensor.qscheme()
        if qscheme == torch.per_channel_affine:
            scale, zero_point, axis = (
                qtensor.q_per_channel_scales(),
                qtensor.q_per_channel_zero_points(),
                qtensor.q_per_channel_axis(),
            )
        else:
            scale, zero_point, axis = (
                qtensor.q_scale(),  # type: ignore[assignment]
                qtensor.q_zero_point(),  # type: ignore[assignment]
                None,
            )
        dtype = tensor.dtype
        qmin, qmax = get_qmin_qmax(dtype)
        return get_dequantized(
            tensor, scale, zero_point, qmin, qmax, dtype, axis, qscheme
        )
    return tensor

