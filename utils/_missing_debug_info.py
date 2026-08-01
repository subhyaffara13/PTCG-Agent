
def _missing_debug_info(for_what: str) -> DebugInfo:
  warnings.warn(
      f"{for_what} is missing a DebugInfo object. "
      "This behavior is deprecated, use api_util.debug_info() to "
      "construct a proper DebugInfo object and propagate it to this function. "
      "See https://github.com/jax-ml/jax/issues/26480 for more details.",
      DeprecationWarning, stacklevel=2)
  return DebugInfo("missing_debug_info", "<missing_debug_info>", None, None)

