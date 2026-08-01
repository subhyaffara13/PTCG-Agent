
def _attention_out_aval(in_aval, shape=None, dtype=None):
  # Build an output abstract value that propagates the varying manual axes
  # (vma) of `in_aval`. Without this, outputs produced inside a `shard_map`
  # (e.g. the gradients from the backward primitive) lose the manual sharding
  # axes carried by their inputs, which makes the custom_vjp backward rule
  # produce cotangents whose type does not match the primal inputs.
  # See https://github.com/jax-ml/jax/issues/36008
  # `shape`/`dtype` default to those of `in_aval` (e.g. gradient outputs match
  # their corresponding input); the forward outputs override them.
  shape = in_aval.shape if shape is None else shape
  dtype = in_aval.dtype if dtype is None else dtype
  if in_aval.mat.empty:
    # Preserve the previous behavior (replicated/empty sharding) outside of
    # manual (shard_map) contexts.
    return core.ShapedArray(shape, dtype)
  return core.ShapedArray(
      shape, dtype, sharding=NamedSharding(in_aval.sharding.mesh, PartitionSpec()),
      manual_axis_type=core.ManualAxisType(varying=in_aval.mat.varying))

