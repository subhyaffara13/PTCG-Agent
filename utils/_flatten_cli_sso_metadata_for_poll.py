
def _flatten_cli_sso_metadata_for_poll(
    metadata: Dict[str, Any],
) -> Dict[str, Union[str, int, float, bool]]:
    """Expose scalar attribution metadata as a flat dict for CLI poll responses."""
    flattened: Dict[str, Union[str, int, float, bool]] = {}
    stack: List[Tuple[str, Any]] = [("", metadata)]
    while stack:
        prefix, value = stack.pop()
        if isinstance(value, dict):
            for key, nested in value.items():
                nested_prefix = f"{prefix}.{key}" if prefix else key
                stack.append((nested_prefix, nested))
        elif _is_safe_cli_sso_scalar_claim_value(value):
            flattened[prefix] = value
    return flattened

