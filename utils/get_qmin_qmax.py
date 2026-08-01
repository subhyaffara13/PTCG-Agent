
def get_qmin_qmax(dtype: torch.dtype) -> tuple[int | float, int | float]:
    return calculate_qmin_qmax(None, None, False, dtype, False)  # type: ignore[arg-type]

