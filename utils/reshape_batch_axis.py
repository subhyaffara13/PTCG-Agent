from typing import Any

def reshape_batch_axis(tree: Any, microbatch_size: int, axis: int = 0) -> Any:
  """Reshape batch axis of pytree leaves for use with microbatching.

  This function reshapes the batch axis of each leaf into a shape
  (num_microbatches, microbatch_size) appearing at the same axis as the original
  batch axis. The reshape is done using a column-major order, so any sharding
  along the batch axis should be preserved in the new `microbatch_size` axis,
  while the new `num_microbatches` axis will generally be replicated.

  Args:
    tree: A pytree of jax.Arrays, each having a batch axis.
    microbatch_size: The size of sub-batches used for each microbatch.
    axis: The axis to reshape.

  Returns:
    A pytree of reshaped jax.Arrays.
  """
  def reshape_leaf(x):
    new_shape = x.shape[:axis] + (-1, microbatch_size) + x.shape[axis + 1:]
    if jax.__version__ < '0.7.0':
      return x.reshape(new_shape, order='F')

    sharding = jax.typeof(x).sharding
    if not sharding.mesh.are_all_axes_explicit:
      return x.reshape(new_shape, order='F')

    assert jax.__version__ >= '0.8.1', (
        'microbatching with explicit sharding requires jax version >= 0.8.1.'
    )
    spec = sharding.spec
    if len(spec) < axis:  # The batch axis is not sharded.
      new_spec = spec
    else:
      new_spec = jax.P(*spec[:axis], None, spec[axis], *spec[axis + 1:])
    out_sharding = jax.sharding.NamedSharding(sharding.mesh, new_spec)

    local_shape = sharding.shard_shape(x.shape)
    nshards = x.shape[axis] // local_shape[axis]
    if microbatch_size % nshards != 0:
      raise ValueError(f'{nshards=} must evenly divide {microbatch_size=}.')

    return x.reshape(new_shape, order='F', out_sharding=out_sharding)

  return jax.tree.map(reshape_leaf, tree)

