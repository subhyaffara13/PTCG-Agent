
def _is_flax_summary(value: Array) -> bool:
  if 'flax.linen' not in sys.modules:
    return False
  from flax import linen as nn  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error

  return isinstance(value, nn.summary._ArrayRepresentation)  # pylint: disable=protected-access

