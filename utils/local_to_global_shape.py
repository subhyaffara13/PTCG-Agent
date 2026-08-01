
def local_to_global_shape(
    sharding: jsharding.Sharding, local_shape: Shape) -> tuple[int | None, ...]:
  """Computes the global shape given the per process if possible.

  The returned shape will have the size of the global tensor in that dimension
  or None, if it is not computable. The latter can happen when sharding
  is not uniform along that dimension, e.g. different hosts require
  different shapes, or if different processes have partial data overlap.

  If at most one dimension is sharded the shape is always computable.
  Generally, global shape is computable for most practical meshes (including
  topology aware such as meshes returned by mesh_utils.create_device_mesh)

  Some examples: Suppose mesh is {'a': 2, 'b': 2, 'c': 2} with 2 devices
  per host, 4 hosts total. For different specs we get:
  - P():
      global_shape = local_shape

  - P(('a', 'b', 'c'), None):
      global_shape =  (4 * local_shape[0], local_shape[1])
      Note: per device shape is (local_shape[0] / 2, local_shape[1])

  - P(('a', 'b'), None)
      global_shape =  (4 * local_shape[0], local_shape[1])
      # NB: the same global shape as above, since sharding along 'c' dimension
      # happens to be within process, and thus doesn't affect the global shape.
      # The underlying difference will be in the per *device* shape, which
      # would be  (local_shape[0], local_shape[1]) in this case.

  - P(None, ('a', 'c'))
      global_shape = (local_shape[0], 2 * local_shape[1])
      # Per device shape is (local_shape[0], local_shape[1] / 2)
  - P(('a', 'c'), 'b'):
      global_shape = (2 * local_shape[0], 2 * local_shape[1])
      # Per device shape is (local_shape[0] / 2, local_shape[1])
  - If devices in the Mesh are randomly permuted: For any partition spec
  which shards more than 1 axis:  e.g. P('a', ('b', 'c')):
      global_shape = (None, None)

  Args:
    local_shape: global shape of the tensor.

  Returns:
    global_shape with Nones in non-uniform dimensions.
  """

  global_shape : list[int | None] = [None] * len(local_shape)
  for i, local_dim in enumerate(local_shape):
    try:
      _, shard_count = get_process_index_and_count(
          sharding, i, ndims=len(local_shape))
      global_shape[i] = local_dim * shard_count
    except NonUniformShardingError:
      global_shape[i] = None
      continue

  return tuple(global_shape)

