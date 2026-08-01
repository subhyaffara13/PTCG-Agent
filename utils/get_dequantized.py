
def get_dequantized(
    val: torch.Tensor,
    scale: float | torch.Tensor,
    zero_point: float | torch.Tensor,
    qmin: float | int,
    qmax: float | int,
    dtype: torch.dtype,
    axis: int | None,
    qscheme: torch.qscheme | None,
) -> torch.Tensor:
    if qscheme is torch.per_tensor_affine:
        return dequantize_per_tensor(
            val,
            scale,  # type: ignore[arg-type]
            zero_point,  # type: ignore[arg-type]
            qmin,  # type: ignore[arg-type]
            qmax,  # type: ignore[arg-type]
            dtype,
        )
    elif qscheme is torch.per_channel_affine:
        return dequantize_per_channel(
            val,
            scale,  # type: ignore[arg-type]
            zero_point,  # type: ignore[arg-type]
            axis,  # type: ignore[arg-type]
            qmin,  # type: ignore[arg-type]
            qmax,  # type: ignore[arg-type]
            dtype,
        )
    else:
        raise RuntimeError(f"Unsupported dequantization scheme: {qscheme}")

