
def _get_registry():
    global _registry
    if _registry is None:
        from cb_agents.card_registry import CardRegistry
        _registry = CardRegistry()
    return _registry


def _get_registry():
    global _registry
    if _registry is None:
        from cb_agents.card_registry import CardRegistry
        _registry = CardRegistry()
    return _registry


def _get_registry():
    global _registry
    if _registry is None:
        from cb_agents.card_registry import CardRegistry
        _registry = CardRegistry()
    return _registry


def _get_registry():
    global _registry
    if _registry is None:
        from cb_agents.card_registry import CardRegistry
        _registry = CardRegistry()
    return _registry


def _get_registry(module: nn.Module) -> dict[str, RegistryItem] | None:
    r"""
    Get an ``OrderedDict`` of composable APIs that have been applied to the
    ``module``, indexed by the API name. If no API has been applied, then this
    returns ``None``.
    """
    return getattr(module, REGISTRY_KEY, None)


def _get_registry() -> Registry:
    """Return the harness registry, loading (and caching in-process) on first call.

    Best-effort: any unexpected error degrades to an empty registry so detection
    never raises.
    """
    global _registry
    if _registry is None:
        try:
            _registry = _load_registry()
        except Exception:
            logger.debug("Could not resolve agent harnesses registry.", exc_info=True)
            _registry = _EMPTY_REGISTRY
    return _registry

