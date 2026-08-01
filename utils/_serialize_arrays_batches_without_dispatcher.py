
def _serialize_arrays_batches_without_dispatcher(
    prioritized: Sequence[tuple[jax.Array, types.ParamInfo, types.SaveArgs]],
    deprioritized: Sequence[tuple[jax.Array, types.ParamInfo, types.SaveArgs]],
    device_host_max_bytes: int | None,
    replica_id: int | None,
    use_replica_parallel: bool,
    min_slice_bytes_for_replica_parallel: int | None,
    max_replicas_for_replica_parallel: int | None,
    primary_host: int | None,
    metadata_key: str | None,
    array_metadata_store: array_metadata_store_lib.Store | None,
    enable_replica_parallel_separate_folder: bool,
    ext_metadata: Dict[str, Any],
    enable_pinned_host_transfer: bool,
    callback: types.SerializationStatusCallback,
) -> future.Future:
  """Serializes arrays batches without dispatcher."""
  # Complete D2H transfer in parallel for each array for prioritized values.
  replica_slices_transfer_arrays_to_host = functools.partial(
      replica_slices.transfer_arrays_to_host,
      replica_id=replica_id,
      use_replica_parallel=use_replica_parallel,
      enable_pinned_host_transfer=enable_pinned_host_transfer,
      min_slice_bytes_for_replica_parallel=min_slice_bytes_for_replica_parallel,
      max_replicas_for_replica_parallel=max_replicas_for_replica_parallel,
  )
  async_serialize_replica_slices_batch = functools.partial(
      _async_serialize_replica_slices,
      primary_host=primary_host,
      metadata_key=metadata_key,
      array_metadata_store=array_metadata_store,
      enable_replica_parallel_separate_folder=enable_replica_parallel_separate_folder,
      use_replica_parallel=use_replica_parallel,
      ext_metadata=ext_metadata,
  )
  prioritized_values_on_host = []
  prioritized_infos = []
  prioritized_args = []
  if prioritized:
    logging.info(
        'Scheduling D2H of %d prioritized jax.Array.',
        len(prioritized),
    )
    prioritized_arrays, prioritized_infos, prioritized_args = zip(*prioritized)
    prioritized_values_on_host = replica_slices_transfer_arrays_to_host(
        prioritized_arrays
    )
    _on_batch_callback(prioritized_infos, callback.on_transfer_end)
  else:
    logging.warning(
        'No prioritized params found for saving. D2H for all values will be'
        ' scheduled asynchronously.'
    )

  async def _serialize_without_dispatcher():
    if not prioritized and not deprioritized:
      return
    try:
      initial_ts_metrics = ts.experimental_collect_matching_metrics(
          '/tensorstore/'
      )
    except Exception:  # pylint: disable=broad-except
      initial_ts_metrics = None
    total_start_time = time.time()
    logical_bytes = 0

    if prioritized_values_on_host:
      logical_bytes += sum(v.nbytes for v in prioritized_values_on_host)
      await async_serialize_replica_slices_batch(
          prioritized_values_on_host,
          prioritized_infos,
          prioritized_args,
      )
      _on_batch_callback(prioritized_infos, callback.on_write_end)
    if deprioritized:
      assert device_host_max_bytes is not None
      for (
          b_arrays,
          b_infos,
          b_args,
      ) in _get_deprioritized_batches_to_serialize(
          deprioritized,
          device_host_max_bytes=device_host_max_bytes,
          # TODO(b/436858989): We overestimate memory usage for now if replica
          # parallel is enabled, as each host has a non-trivial calculation for
          # bytes transferred to host.
          replica_id=None if use_replica_parallel else replica_id,
          dispatcher=None,
      ):
        b_arrays_on_host = replica_slices_transfer_arrays_to_host(b_arrays)
        _on_batch_callback(b_infos, callback.on_transfer_end)
        logical_bytes += sum(v.nbytes for v in b_arrays_on_host)
        await async_serialize_replica_slices_batch(
            b_arrays_on_host,
            b_infos,
            b_args,
        )
        _on_batch_callback(b_infos, callback.on_write_end)

    info_sample = prioritized[0][1] if prioritized else deprioritized[0][1]
    _log_io_metrics(
        direction=types.IoDirection.WRITE,
        logical_bytes=logical_bytes,
        start_time=total_start_time,
        parent_dir=info_sample.parent_dir,
        initial_ts_metrics=initial_ts_metrics,
    )

  return future.CommitFutureAwaitingContractedSignals(
      _serialize_without_dispatcher(),
      name='array_type_handler',
  )

