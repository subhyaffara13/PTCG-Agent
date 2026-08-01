
def _are_both_of_mapping_type(a: object, b: object) -> bool:
  return isinstance(a, abc.Mapping) and isinstance(
      b, abc.Mapping)

