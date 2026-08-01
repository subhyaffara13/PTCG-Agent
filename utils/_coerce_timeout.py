
def _coerce_timeout(value: Any, fallback: float) -> float:
    """Return `value` if it is a real int/float, else `fallback`. Guards
    against tests that mock `prisma_client` and leave the timeout slots as
    MagicMock instances."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return fallback

