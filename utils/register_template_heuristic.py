
def register_template_heuristic(
    template_name: str,
    device_type: str | None,
    register: bool = True,
    op_name: str | None = None,
) -> Any:
    """
    Decorator to register template heuristic classes.

    Args:
        template_name: Name of the template (e.g., "mm", "bmm", "scaled_mm")
        device_type: Device type ("cuda", "cpu", "xpu")
            Set this to None to indicate that the heuristic is applicable to all device types.
        register: Whether to register this heuristic. Caller should pass the condition directly.
        op_name: Name of the operator (e.g., "mm", "bmm", "scaled_mm"). This is optional
            and is only used when a template uses different heuristics for different ops

    Returns:
        Decorator function that registers the class if conditions are met.

    Example:
        @register_template_heuristic("mm", "cuda", register=torch.version.hip is None)
        class CUDAMMTemplateConfigHeuristic(MMTemplateConfigMixin, CUDAConfigHeuristic):
            pass
    """

    def decorator(
        cls: type[TemplateConfigHeuristics],
    ) -> type[TemplateConfigHeuristics]:
        if register:
            key: tuple[str | None, ...] = (template_name, device_type, op_name)
            _TEMPLATE_HEURISTIC_REGISTRY[key] = cls
            log.info(
                f"Registered template heuristic: {cls.__name__} for '{template_name=}', '{device_type=}', '{op_name=}'"  # noqa: G004
            )
        return cls

    return decorator

