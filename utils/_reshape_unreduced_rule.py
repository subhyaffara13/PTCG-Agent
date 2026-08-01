
def _reshape_unreduced_rule(operand, *, new_sizes, dimensions, sharding):
  op_unreduced = getu(operand)
  if op_unreduced:
    if (sharding is not None and
        operand.sharding.spec.unreduced != sharding.spec.unreduced):  # Explicit mode
      raise ValueError(
          'out_sharding passed to reshape must be unreduced over the same mesh'
          f' axes as operand. Got out_sharding: {sharding.spec} and operand'
          f' type: {operand.str_short(True)}')
    return op_unreduced
  if sharding is not None and sharding.spec.unreduced:
    raise ValueError('out_sharding passed to `reshape` cannot contain '
                     f'unreduced axes. Got {sharding}')
  return op_unreduced

