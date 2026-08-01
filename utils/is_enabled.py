
def is_enabled() -> bool:
    r"""Returns whether the TunableOp feature is enabled."""
    return torch._C._cuda_tunableop_is_enabled()  # type: ignore[attr-defined]


def is_enabled() -> bool:
    """
    Check if observability is enabled.

    Returns:
        True if metrics are being collected, False otherwise
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()

    return _metrics_collector is not None

