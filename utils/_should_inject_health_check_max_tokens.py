
def _should_inject_health_check_max_tokens(
    model_info: Mapping[str, object], mode: str | None
) -> bool:
    """
    Whether the health-check probe should include `max_tokens`.

    Order:
      1. `model_info.health_check_supports_max_tokens` (operator override).
      2. `_MAX_TOKEN_SUPPORT_MODES`. An unresolvable mode is treated as `chat`
         for backward compatibility.
    """
    explicit = model_info.get("health_check_supports_max_tokens")
    if explicit is not None:
        return bool(explicit)
    return (mode or "chat") in _MAX_TOKEN_SUPPORT_MODES

