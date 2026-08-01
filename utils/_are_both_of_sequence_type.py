
def _are_both_of_sequence_type(a: object, b: object) -> bool:
  return isinstance(a, abc.Sequence) and isinstance(
      b, abc.Sequence) and not isinstance(
          a, _TEXT_OR_BINARY_TYPES) and not isinstance(b, _TEXT_OR_BINARY_TYPES)

