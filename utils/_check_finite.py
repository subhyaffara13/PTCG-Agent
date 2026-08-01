
def _check_finite(array: Array, xp: ModuleType) -> None:
    """Check for NaNs or Infs."""
    if not xp.all(xp.isfinite(array)):
        msg = "array must not contain infs or NaNs"
        raise ValueError(msg)

