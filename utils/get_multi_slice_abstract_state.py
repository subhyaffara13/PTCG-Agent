
def get_multi_slice_abstract_state(
    context: ocp.Context,
    global_mesh: jax.sharding.Mesh,
    *,
    reference_checkpoint_path: epath.Path,
    reference_sharding_path: epath.Path,
) -> Any:
  """Returns the abstract state for all replicas."""
  with ocp.Context(context=context):
    metadata = ocp.metadata(reference_checkpoint_path)
    # Abstract tree has shardings on a single replica.
    single_replica_abstract_state = (
        checkpoint_generation.get_abstract_state_from_sharding_config(
            reference_sharding_path,
            metadata.metadata,
            devices=multislice.replica_devices(
                global_mesh, replica_id=0, replica_axis_index=0
            ).tolist(),
        )
    )

    # Blow shardings up to all replicas.
    def _multi_replica_sharding(abstract_arr: jax.ShapeDtypeStruct):
      logging.info(
          "Original (single-replica) sharding: %s", abstract_arr.sharding
      )
      assert isinstance(abstract_arr.sharding, jax.sharding.NamedSharding)
      single_replica_mesh = abstract_arr.sharding.mesh
      single_replica_partition_spec = abstract_arr.sharding.spec
      multi_replica_sharding = jax.sharding.NamedSharding(
          jax.sharding.Mesh(
              devices=global_mesh.devices.reshape(
                  -1, *single_replica_mesh.devices.shape
              ),
              axis_names=["replica", *single_replica_mesh.axis_names],
          ),
          spec=jax.sharding.PartitionSpec(*single_replica_partition_spec),
      )
      logging.info("Multi-replica sharding: %s", multi_replica_sharding)
      return jax.ShapeDtypeStruct(
          shape=abstract_arr.shape,
          dtype=abstract_arr.dtype,
          sharding=multi_replica_sharding,
      )

    return jax.tree.map(
        _multi_replica_sharding,
        single_replica_abstract_state,
    )

