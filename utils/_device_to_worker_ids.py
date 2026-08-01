
def _device_to_worker_ids(dispatcher: dispatchers.Dispatcher) -> dict[int, int]:
  """Returns a mapping from device ID to worker ID.

  Works by using a remote Python function to obtain `multihost.process_index()`
  on
  each worker. This is then returned as a sharded array, where shard `i`,
  located on device `i`, contains the worker ID for which device `i` is local
  (`jax.local_devices()`).

  These contortions are necessary because there is not a straightforward API to
  obtain the mapping on Pathways.

  Args:
    dispatcher: The dispatcher instance to use.

  Returns:
    A mapping from device ID to worker ID.
  """
  fully_sharded_sharding = jax.sharding.NamedSharding(
      jax.sharding.Mesh(jax.devices(), 'x'),
      jax.sharding.PartitionSpec(
          'x',
      ),
  )

  def _get_worker_ids_impl(device_ids: jax.Array) -> jax.Array:
    return jax.make_array_from_callback(
        device_ids.shape,
        device_ids.sharding,
        lambda _: np.array(multihost.process_index()).reshape(
            1,
        ),
        dtype=np.int32,
    )

  device_ids = jax.device_put(
      np.asarray([d.id for d in jax.devices()]),
      device=fully_sharded_sharding,
  )
  result_specs = jax.ShapeDtypeStruct(
      device_ids.shape, dtype=np.int32, sharding=fully_sharded_sharding
  )
  worker_ids = dispatcher.dispatch(
      _get_worker_ids_impl, input_arrays=device_ids, result_specs=result_specs
  )
  jax.block_until_ready(worker_ids)
  return {
      int(device_id): int(worker_id)
      for device_id, worker_id in zip(
          np.asarray(device_ids), np.asarray(worker_ids)
      )
  }

