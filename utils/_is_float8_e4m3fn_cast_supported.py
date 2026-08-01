
def _is_float8_e4m3fn_cast_supported(compute_capability: int | None) -> bool:
  return compute_capability is None or compute_capability >= 89

