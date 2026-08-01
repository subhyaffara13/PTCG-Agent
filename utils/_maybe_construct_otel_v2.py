
def _maybe_construct_otel_v2(
    callback_name: str, _in_memory_loggers: list
) -> Optional[Any]:
    """If ``LITELLM_OTEL_V2`` is on, build (or reuse) a single ``OpenTelemetryV2``
    instance configured via the preset for ``callback_name``.

    Returns ``None`` when V2 is off OR when there's no preset registered for
    ``callback_name`` — callers should then fall through to the legacy path.
    """
    from litellm.integrations.otel.model.config import is_otel_v2_enabled

    if not is_otel_v2_enabled():
        return None
    from litellm.integrations.otel.logger import OpenTelemetryV2
    from litellm.integrations.otel.presets import PRESET_BY_CALLBACK

    preset_fn = PRESET_BY_CALLBACK.get(callback_name)
    if preset_fn is None:
        return None
    for callback in _in_memory_loggers:
        if (
            isinstance(callback, OpenTelemetryV2)
            and getattr(callback, "callback_name", None) == callback_name
        ):
            return callback
    try:
        config = preset_fn()
    except Exception:
        # If env vars are missing or the preset raises, defer to the legacy path
        # so customers get the same error story they had before V2 landed.
        return None
    v2_logger = OpenTelemetryV2(config=config, callback_name=callback_name)
    _in_memory_loggers.append(v2_logger)
    return v2_logger

