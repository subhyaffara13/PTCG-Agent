
def _iter_enabled_fusions(fusion_config: Mapping[str, bool | Mapping[str, Any]]) -> list[str]:
    """Validate `fusion_config` and return enabled fusion names in user-specified order."""

    enabled_fusions = []
    for fusion_name, fusion_options in fusion_config.items():
        if fusion_name not in _FUSION_REGISTRY:
            raise ValueError(f"Unknown fusion type: {fusion_name}")
        if fusion_options is False:
            continue
        if fusion_options is not True and not isinstance(fusion_options, Mapping):
            raise ValueError(
                f"Invalid fusion config for {fusion_name}: expected `True`, `False`, or a mapping of options."
            )
        enabled_fusions.append(fusion_name)
    return enabled_fusions

