
def _scalar_tensor_aten(
    scalar: NumberType,
    *,
    dtype: torch.dtype,
    device: torch.device,
) -> Tensor:
    if isinstance(scalar, complex) and (
        dtype is None or not utils.is_complex_dtype(dtype)
    ):
        raise TypeError("Complex scalar requires complex tensor dtype.")
    # Note that Mypy thinks torch.scalar can't accept a complex scalar
    return torch.scalar_tensor(scalar, dtype=dtype, device=device)  # type: ignore[arg-type]

