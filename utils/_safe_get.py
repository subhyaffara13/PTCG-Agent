
def _safe_get(obj, key, default=None):
    """Read ``key`` from a dict-like or Pydantic-model-like object.

    The arize/langfuse_otel logger receives ``usage`` objects from many sources:
    plain dicts, litellm ``Usage`` (which exposes ``.get``), and raw OpenAI
    Pydantic models (e.g. ``openai.types.completion_usage.CompletionUsage`` and
    nested ``CompletionTokensDetails`` / ``OutputTokensDetails``) which do NOT
    expose ``.get``. Calling ``.get`` on the latter raised ``AttributeError`` —
    see https://github.com/BerriAI/litellm/issues/13672.
    """
    if obj is None:
        return default
    getter = getattr(obj, "get", None)
    if callable(getter):
        try:
            return getter(key, default)
        except TypeError:
            # Some objects expose `.get` with a different signature
            pass
    return getattr(obj, key, default)

