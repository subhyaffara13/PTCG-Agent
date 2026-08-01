
def split_to_logical_devices(tensor: TfVal,
                             partition_dimensions: PartitionsOrReplicated):
  """Like TPUMPStrategy.experimental_split_to_logical_devices.

  For jax2tf purposes we want to avoid needing to thread the `strategy` object
  through the generated computation. It seems that the original function needs
  the strategy object only for error checking, which we assume is done upstream
  by JAX.

  Args:
    tensor: Input tensor to annotate.
    partition_dimensions: A list of integers, with one integer per tensor
      dimension, specifying in how many parts the dimension should be split. The
      product of integers must equal the number of devices per replica.
    use_sharding_op: whether to use a sharding op, or not.

  Returns:
    an annotated tensor.
  """
  # TODO: this is only for sharded_jit. Either remove, or implement in terms
  # of _shard_values.
  if partition_dimensions is None:
    return xla_sharding.replicate(tensor, use_sharding_op=True)
  num_partition_splits = math.prod(partition_dimensions)
  tile_assignment = np.arange(num_partition_splits).reshape(
      partition_dimensions)
  return xla_sharding.tile(tensor, tile_assignment, use_sharding_op=True)

