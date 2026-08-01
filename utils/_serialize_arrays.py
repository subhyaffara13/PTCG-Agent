
def _serialize_arrays(
    arrays: Sequence[jax.Array],
    infos: Sequence[types.ParamInfo],
    args: Sequence[types.SaveArgs],
    dispatcher: dispatchers.Dispatcher | None,
    replica_id: int | None,
    use_replica_parallel: bool,
    min_slice_bytes_for_replica_parallel: int | None,
    max_replicas_for_replica_parallel: int | None,
    primary_host: int | None,
    metadata_key: str | None,
    array_metadata_store: array_metadata_store_lib.Store | None,
    enable_replica_parallel_separate_folder: bool,
    ext_metadata: Dict[str, Any],
    callback: types.SerializationStatusCallback,
) -> future.Future:
  """D2H transfer and serialize arrays using dispatcher if provided."""

  device_host_max_bytes = None
  if byte_limiter := infos[0].device_host_byte_limiter:
    if isinstance(byte_limiter, limits.LimitInFlightBytes):
      device_host_max_bytes = byte_limiter.max_bytes

  prioritized: list[tuple[jax.Array, types.ParamInfo, types.SaveArgs]] = []
  prioritized_async: list[tuple[jax.Array, types.ParamInfo, types.SaveArgs]] = (
      []
  )
  deprioritized: list[tuple[jax.Array, types.ParamInfo, types.SaveArgs]] = []

  if device_host_max_bytes is None:
    for info, arg, value in zip(infos, args, arrays):
      prioritized.append((value, info, arg))
  else:
    for info, arg, value in zip(infos, args, arrays):
      prioritization = callback.key_priority(info.keypath)
      if prioritization == types.TransferPriority.SYNCHRONOUS:
        prioritized.append((value, info, arg))
      elif prioritization == types.TransferPriority.ASYNCHRONOUS_PRIORITIZED:
        prioritized_async.append((value, info, arg))
      elif prioritization == types.TransferPriority.ASYNCHRONOUS_DEPRIORITIZED:
        deprioritized.append((value, info, arg))
      elif prioritization == types.TransferPriority.UNKNOWN:
        raise ValueError(
            f'Prioritization is unknown for key {info.keypath}.'
        )

  deprioritized = prioritized_async + deprioritized

  if dispatcher is None:
    return _serialize_arrays_batches_without_dispatcher(
        prioritized,
        deprioritized,
        device_host_max_bytes,
        replica_id,
        use_replica_parallel,
        min_slice_bytes_for_replica_parallel,
        max_replicas_for_replica_parallel,
        primary_host,
        metadata_key,
        array_metadata_store,
        enable_replica_parallel_separate_folder,
        ext_metadata,
        infos[0].enable_pinned_host_transfer,
        callback,
    )
  else:

    def _serialize_batch(
        batch_infos: Sequence[types.ParamInfo],
        batch_args: Sequence[types.SaveArgs],
        batch_arrays: Sequence[jax.Array],
    ):
      ret = dispatcher.dispatch(
          _worker_serialize_arrays,
          input_arrays=batch_arrays,
          func_kwargs={
              'infos': batch_infos,
              'args': batch_args,
              'replica_id': replica_id,
              'use_replica_parallel': use_replica_parallel,
              'min_slice_bytes_for_replica_parallel': (
                  min_slice_bytes_for_replica_parallel
              ),
              'max_replicas_for_replica_parallel': (
                  max_replicas_for_replica_parallel
              ),
              'primary_host': primary_host,
              'metadata_key': metadata_key,
              'array_metadata_store': array_metadata_store,
              'enable_replica_parallel_separate_folder': (
                  enable_replica_parallel_separate_folder
              ),
              'ext_metadata': ext_metadata,
          },
      )
      _on_batch_callback(batch_infos, callback.on_transfer_end)

      jax.block_until_ready(ret)

      _on_batch_callback(batch_infos, callback.on_write_end)

    # Enqueue D2H operation for prioritized values.
    if prioritized:
      logging.info(
          'Scheduling D2H of %d prioritized jax.Array.',
          len(prioritized),
      )
      prioritized_arrays, prioritized_infos, prioritized_args = zip(
          *prioritized
      )
      prioritized_arrays = dispatcher.device_to_host(prioritized_arrays)
      prioritized = [
          (v, i, a)
          for v, i, a in zip(
              prioritized_arrays, prioritized_infos, prioritized_args
          )
      ]
    else:
      logging.warning(
          'No prioritized params found for saving. D2H for all values will be'
          ' scheduled asynchronously.'
      )

    all_infos = infos

    async def _serialize():
      for info in all_infos:
        await info.await_path_creation()
      if prioritized:
        arrays, infos, args = zip(*prioritized)
        _serialize_batch(infos, args, arrays)
      if deprioritized:
        assert device_host_max_bytes is not None
        for (
            b_arrays,
            b_infos,
            b_args,
        ) in _get_deprioritized_batches_to_serialize(
            deprioritized,
            device_host_max_bytes=device_host_max_bytes,
            replica_id=replica_id,
            dispatcher=dispatcher,
        ):
          _serialize_batch(b_infos, b_args, b_arrays)

    return future.CommitFutureAwaitingContractedSignals(
        _serialize(),
        name='array_type_handler',
    )

