
def transfer_arrays_to_host(
    arrays: Sequence[jax.Array],
    replica_id: Optional[int],
    use_replica_parallel: bool,
    min_slice_bytes_for_replica_parallel: Optional[int] = None,
    max_replicas_for_replica_parallel: Optional[int] = None,
    *,
    enable_pinned_host_transfer: bool = False,
) -> Sequence[ReplicaSlices]:
  """Transfers arrays to host memory.

  Transfers jax.Arrays to host memory and returns all the fragments to be
  serialized by the given replica, along with local shape. Blocks until
  completion.

  Args:
    arrays: The jax.Arrays to transfer.
    replica_id: Configured replica_id.
    use_replica_parallel: Whether to use replica-parallel serialization to allow
      arrays with replicated shards to be written cooperatively by different
      hosts.
    min_slice_bytes_for_replica_parallel: Minimum number of bytes per replica
      slice. Only uses replica-parallel when the amount of data written per
      replica is greater than or equal to this number.
    max_replicas_for_replica_parallel: Maximum number of replicas over which to
      parallelize the writing of replicated shards if use_replica_parallel is
      True.
    enable_pinned_host_transfer: Whether to allow transfer to pinned host
      memory. Pinned memory is closely associated with a TPU device and can

  Returns:
    ReplicaSlices objects, in host memory.
  """
  logging.info(
      'Transferring arrays to host memory with options:'
      ' use_replica_parallel=%s, min_slice_bytes_for_replica_parallel=%s,'
      ' max_replicas_for_replica_parallel=%s, enable_pinned_host_transfer=%s',
      use_replica_parallel,
      min_slice_bytes_for_replica_parallel,
      max_replicas_for_replica_parallel,
      enable_pinned_host_transfer,
  )

  def use_pinned_host_transfer(device: jax.Device):
    has_pinned_host = any(
        m.kind == 'pinned_host' for m in device.addressable_memories()
    )
    return enable_pinned_host_transfer and has_pinned_host

  def async_transfer_slice(
      rslice: ReplicaSlice,
  ) -> tuple[ReplicaSlice, jax.Array]:
    assert not rslice.is_on_host
    data = rslice.data()
    assert isinstance(data, jax.Array)
    device = data.device
    # Start the asynchronous device-to-host copy
    if use_pinned_host_transfer(device):
      # If available, transfer to pinned host memory
      data = jax.device_put(
          data,
          make_single_device_sharding(device, memory_kind='pinned_host'),
      )
    else:
      data.copy_to_host_async()
    return rslice, data

  # Gather the replica slices to be saved for each array.
  rslices_per_array = [
      get_replica_slices(
          arr,
          replica_id,
          use_replica_parallel,
          min_slice_bytes_for_replica_parallel,
          max_replicas_for_replica_parallel,
      )
      for arr in arrays
  ]
  # Kick off transfers for all replica slices to be saved.
  transfers_per_array = [
      [async_transfer_slice(rslice) for rslice in rslices.replica_slices]
      for rslices in rslices_per_array
  ]
  # Wait for all the transferred data to be ready.
  return [
      dataclasses.replace(
          rslices,
          is_on_host=True,
          replica_slices=[
              dataclasses.replace(
                  rslice_on_device,
                  # Conversion to numpy arrays forces block_until_ready.
                  unsliced_data=np.asarray(data),
                  slice_args=None,
              )
              for rslice_on_device, data in transfers
          ],
      )
      for rslices, transfers in zip(rslices_per_array, transfers_per_array)
  ]

