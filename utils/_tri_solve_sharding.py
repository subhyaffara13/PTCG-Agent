
def _tri_solve_sharding(a, b, *, left_side, lower, transpose_a, conjugate_a,
                        unit_diagonal):
  del lower, conjugate_a, unit_diagonal
  batch_spec,  a_spec = a.sharding.spec[:-2], a.sharding.spec[-2:]
  batch_spec_, b_spec = b.sharding.spec[:-2], b.sharding.spec[-2:]
  if batch_spec != batch_spec_:
    raise core.ShardingTypeError(
        "All inputs to triangular_solve must have the same batch sharding, "
        f"but got {batch_spec} and {batch_spec_}.")
  if a_spec[left_side ^ transpose_a] is not None:
    raise core.ShardingTypeError(
        "triangular solve input `a` must be unsharded on the contracting axis, "
        f"but got {a.sharding.spec} with {left_side=} and {transpose_a=}.")
  if b_spec[not left_side] is not None:
    raise core.ShardingTypeError(
        "triangular solve input `b` must be unsharded on the contracting axis, "
        f"but got {b.sharding.spec} with {left_side=} and {transpose_a=}.")
  out_spec = ([a_spec[transpose_a], b_spec[1]] if left_side else
              [b_spec[0], a_spec[not transpose_a]])
  return a.sharding.update(spec=P(*batch_spec, *out_spec))

