
def _trilu_checks(
    name: str,
    row: int,
    col: int,
    dtype: torch.dtype,
    layout: torch.layout,
    pin_memory: bool,
):
    torch._check(row >= 0, lambda: f"row must be non-negative, got {row}")
    torch._check(col >= 0, lambda: f"col must be non-negative, got {col}")
    torch._check(
        dtype in (torch.int32, torch.int64),
        lambda: f"\"{name}\" not implemented for '{dtype}'",
    )

