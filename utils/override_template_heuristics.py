
def override_template_heuristics(
    device_type: str,
    template_op_pairs: list[tuple[str, str]],
    override_heuristic_class: type[TemplateConfigHeuristics] = TemplateConfigHeuristics,
) -> Iterator[None]:
    """
    Context manager to temporarily override template heuristics.

    This is useful for testing purposes, where we want to ensure a specific template/op pair
    uses a custom heuristic or returns no entries.

    Args:
        device_type: Device type ("cuda", "cpu", "xpu")
        template_op_pairs: List of (template_name, op_name) pairs to override.
        override_heuristic_class: Heuristic class to use for the override.
            Defaults to TemplateConfigHeuristics (which returns no entries).
    """
    # Save original entries to restore later
    original_entries = {}
    new_keys = []
    _HEURISTIC_CACHE.clear()
    try:
        for template_name, op_name in template_op_pairs:
            assert op_name is not None
            key = (template_name, device_type, op_name)
            if key in _TEMPLATE_HEURISTIC_REGISTRY:
                original_entries[key] = _TEMPLATE_HEURISTIC_REGISTRY[key]
            _TEMPLATE_HEURISTIC_REGISTRY[key] = override_heuristic_class
            new_keys.append(key)
        yield
    finally:
        # Restore original entries or remove if they didn't exist before
        for key in new_keys:
            _TEMPLATE_HEURISTIC_REGISTRY.pop(key, None)
            if key in original_entries:
                _TEMPLATE_HEURISTIC_REGISTRY[key] = original_entries[key]
        _HEURISTIC_CACHE.clear()

