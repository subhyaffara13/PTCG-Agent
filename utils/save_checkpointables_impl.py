
def save_checkpointables_impl(
    path: path_types.PathLike,
    checkpointables: dict[str, Any],
    *,
    async_origin: bool,
    overwrite: bool,
    custom_metadata: tree_types.JsonType | None,
    partial_save: bool = False,
) -> async_types.AsyncResponse[None]:
  """See caller docstrings."""
  validation.validate_save_checkpointables(checkpointables)
  start_time = time.time()
  event_tracking.OperationRecorder(
      path,
      operation_type=event_tracking.OperationType.SAVE,
      async_origin=async_origin,
  ).record_start(start_time)
  context = context_lib.get_context()
  # Ensure the operation ID is incremented as soon as possible. This must be
  # done uniquely for each save operation.
  asyncio_utils.run_sync(
      synchronization.synchronize_next_operation_id(
          prefix=context.multiprocessing_options.barrier_sync_key_prefix,
          processes=context.multiprocessing_options.active_processes,
      )
  )

  path = context.file_options.path_class(path)
  _check_directory_consistency(path)
  # Prevent internal mutation from affecting the caller.
  checkpointables = dict(checkpointables)
  checkpointables = add_internal_checkpointables(
      checkpointables, context=context
  )
  snapshot_type = snapshot_lib.SnapshotType.EMPTY if partial_save else None
  temporary_path = _TemporaryPathAwaitingCreation(
      path,
      subdirectories=checkpointables.keys(),
      snapshot_type=snapshot_type,
  )
  background_awaitable = asyncio_utils.run_sync(
      _run_blocking_save(
          temporary_path,
          checkpointables,
          overwrite=overwrite,
          context=context,
          partial_save=partial_save,
      )
  )
  return _SaveResponse.create(
      background_awaitable,
      checkpointables,
      temporary_path,
      start_time,
      context=context,
      custom_metadata=custom_metadata,
      async_origin=async_origin,
      partial_save=partial_save,
  )

