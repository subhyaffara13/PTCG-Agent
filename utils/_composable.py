
def _composable(module: nn.Module) -> bool:
    """
    Returns if ``module`` can compose with ``fully_shard``.
    """
    # TODO: Add any other composable APIs that are mutually exclusive.
    registry = _get_registry(module)
    if registry is None:
        return True
    return "replicate" not in registry

