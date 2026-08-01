
def get_registered_heuristic_class(
    template_name: str, device_type: str, op_name: str
) -> None | type[TemplateConfigHeuristics]:
    """
    Get the heuristic class registered for the given template/device/op combination.

    This is useful for creating custom heuristics that subclass the appropriate
    base class for a given template/device/op combination.

    Args:
        template_name: Name of the template (e.g., "mm", "bmm", "scaled_mm")
        device_type: Device type ("cuda", "cpu", "xpu")
        op_name: Name of the operator (e.g., "mm", "bmm", "scaled_mm")

    Returns:
        The heuristic class if found, None otherwise.
    """
    keys = [
        # everything is specified
        (template_name, device_type, op_name),
        # heuristic is valid across all devices
        (template_name, None, op_name),
        # heuristic is valid across all ops for that device
        (template_name, device_type, None),
        # heuristic is always valid for that template
        (template_name, None, None),
    ]
    for key in keys:
        if key in _TEMPLATE_HEURISTIC_REGISTRY:
            return _TEMPLATE_HEURISTIC_REGISTRY[key]

    return None

