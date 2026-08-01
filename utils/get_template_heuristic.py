
def get_template_heuristic(
    template_name: str, device_type: str, op_name: str
) -> TemplateConfigHeuristics:
    """
    Retrieve a template heuristic instance for the given template and device type.

    Args:
        template_name: Name of the template (e.g., "mm", "bmm", "scaled_mm")
        device_type: Device type ("cuda", "cpu", "xpu")
        op_name: Name of the operator (e.g., "mm", "bmm", "scaled_mm")

    Returns:
        Template heuristic instance. If no specific heuristic is found,
        returns a fallback TemplateConfigHeuristics() instance (uncached).
    """
    # Check cache first
    cache_key = (template_name, device_type, op_name)
    if cache_key in _HEURISTIC_CACHE:
        return _HEURISTIC_CACHE[cache_key]

    heuristic_class = get_registered_heuristic_class(
        template_name, device_type, op_name
    )

    if heuristic_class is None:
        # Log error and return fallback instance (uncached)
        log.error(
            "No template heuristic found - template_name=%s, device_type=%s, op_name=%s. "
            "Available combinations: %s. Using fallback TemplateConfigHeuristics instance.",
            template_name,
            device_type,
            op_name,
            list(_TEMPLATE_HEURISTIC_REGISTRY.keys()),
        )
        return TemplateConfigHeuristics()

    # Cache successful lookup and return
    instance = heuristic_class()
    _HEURISTIC_CACHE[cache_key] = instance
    return instance

