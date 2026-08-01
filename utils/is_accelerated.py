
def is_accelerated(deprecation_id: str) -> bool:
  if deprecation_id not in _registered_deprecations:
    raise ValueError(f"{deprecation_id=!r} not registered.")
  return _registered_deprecations[deprecation_id].accelerated

