
def _reshape_reduced_rule(operand, *, new_sizes, dimensions, sharding):
  op_reduced = getr(operand)
  if op_reduced:
    if (sharding is not None and
        operand.sharding.spec.reduced != sharding.spec.reduced):  # Explicit mode
      raise ValueError(
          'out_sharding passed to reshape must be reduced over the same mesh'
          f' axes as operand. Got out_sharding: {sharding.spec} and operand'
          f' type: {operand.str_short(True)}')
    return op_reduced
  if sharding is not None and sharding.spec.reduced:
    raise ValueError('out_sharding passed to `reshape` cannot contain '
                     f'reduced axes. Got {sharding}')
  return op_reduced

