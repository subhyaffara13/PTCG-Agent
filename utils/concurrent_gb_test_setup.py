
def concurrent_gb_test_setup():
  """Setup for tests exercising concurrent_gb setting."""
  # Need to override later so we can use a small number of bytes.
  handler = PyTreeCheckpointHandler(
      save_concurrent_gb=1, restore_concurrent_gb=1, use_ocdbt=False
  )

  mesh = jax.sharding.Mesh(
      jax.devices(),
      ('x',),
  )
  pspec = jax.sharding.PartitionSpec(
      None,
  )

  def _create_sharded_array(arr):
    return create_sharded_array(arr, mesh, pspec)

  # 4 arrays, each has a single chunk, with 4 bytes each.
  tree = jax.tree.map(
      _create_sharded_array,
      {
          'a': np.arange(1, dtype=np.int32),
          'b': np.arange(1, dtype=np.int32),
          'c': np.arange(1, dtype=np.int32),
          'd': np.arange(1, dtype=np.int32),
      },
  )
  restore_args = jax.tree.map(
      lambda _: type_handlers.ArrayRestoreArgs(
          sharding=jax.sharding.NamedSharding(mesh, pspec)
      ),
      tree,
  )
  return handler, tree, restore_args

