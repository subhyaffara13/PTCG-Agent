
def create_train_state(global_mesh: jax.sharding.Mesh) -> PyTree:
  """Create a fake train state for testing."""
  dim_size = 32
  train_state = {
      'a_1d': test_utils.create_sharded_array(
          np.arange(dim_size), global_mesh, jax.sharding.PartitionSpec(None)
      ),
      'b_1d': test_utils.create_sharded_array(
          np.arange(dim_size),
          global_mesh,
          jax.sharding.PartitionSpec('tensor'),
      ),
      'c_2d': test_utils.create_sharded_array(
          np.arange(dim_size**2).reshape((dim_size, dim_size)),
          global_mesh,
          jax.sharding.PartitionSpec(None, 'tensor'),
      ),
      'd_2d': test_utils.create_sharded_array(
          np.arange(dim_size**2).reshape((dim_size, dim_size)),
          global_mesh,
          jax.sharding.PartitionSpec('tensor', None),
      ),
      'e_2d': test_utils.create_sharded_array(
          np.arange(dim_size**2).reshape((dim_size, dim_size)),
          global_mesh,
          jax.sharding.PartitionSpec('tensor', 'fsdp'),
      ),
      'f_2d': test_utils.create_sharded_array(
          np.arange(dim_size**2).reshape((dim_size, dim_size)),
          global_mesh,
          jax.sharding.PartitionSpec('fsdp', 'tensor'),
      ),
      'g_2d': test_utils.create_sharded_array(
          np.arange(dim_size**2).reshape((dim_size, dim_size)),
          global_mesh,
          jax.sharding.PartitionSpec(None, None),
      ),
      'h_3d': test_utils.create_sharded_array(
          np.arange(dim_size**3).reshape((dim_size, dim_size, dim_size)),
          global_mesh,
          jax.sharding.PartitionSpec('tensor', None, 'fsdp'),
      ),
      'i_3d': test_utils.create_sharded_array(
          np.arange(dim_size**3).reshape((dim_size, dim_size, dim_size)),
          global_mesh,
          jax.sharding.PartitionSpec(None, None, 'tensor'),
      ),
      'j_3d': test_utils.create_sharded_array(
          np.arange(dim_size**3).reshape((dim_size, dim_size, dim_size)),
          global_mesh,
          jax.sharding.PartitionSpec(None, None, 'fsdp'),
      ),
      'k_3d': test_utils.create_sharded_array(
          np.arange(dim_size**3).reshape((dim_size, dim_size, dim_size)),
          global_mesh,
          jax.sharding.PartitionSpec(None, None, None),
      ),
      'scalar': test_utils.create_sharded_array(
          123, global_mesh, jax.sharding.PartitionSpec()
      ),
      # Taken from failing MaxText run.
      'custom_array': test_utils.create_sharded_array(
          np.arange(8192 * 64).reshape((8192, 64)),
          global_mesh,
          jax.sharding.PartitionSpec('tensor', None),
      ),
  }
  for k, v in train_state.items():
    _log_array_info(k, v)
  return train_state

