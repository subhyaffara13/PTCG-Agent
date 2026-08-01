
def accelerate(deprecation_id: str) -> None:
  if deprecation_id not in _registered_deprecations:
    raise ValueError(f"{deprecation_id=!r} not registered.")
  _registered_deprecations[deprecation_id].accelerated = True

