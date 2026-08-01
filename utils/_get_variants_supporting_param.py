
def _get_variants_supporting_param(param_name: str) -> list[str]:
  return [
      name
      for name, cls in SUPPORTED_VARIANT_MAP.items()
      if param_name in inspect.signature(cls).parameters.keys()
  ]

