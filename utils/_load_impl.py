import time

def _load_impl(
    path: path_types.Path,
    load_fn: LoadFn,
    start_time: float,
) -> dict[str, Checkpointable] | tree_types.PyTreeOf[tree_types.Leaf]:
  """Implementation of loading logic for both :py:func:`.load_checkpointables` and :py:func:`.load`.

  Args:
    path: The path to the checkpoint.
    load_fn: A  function that returns an awaitable for loading the checkpoint
      based on either :py:func:`.load_checkpointables` or :py:func:`.load`.
    start_time: The time when the loading process started.

  Returns:
    The loaded checkpointables or PyTree itself.
  """
  if not path:
    raise ValueError('Path must not be None.')

  ctx = context_lib.get_context()
  # Ensure the operation ID is incremented as soon as possible. This must be
  # done uniquely for each load operation.
  asyncio_utils.run_sync(
      synchronization.synchronize_next_operation_id(
          prefix=ctx.multiprocessing_options.barrier_sync_key_prefix,
          processes=ctx.multiprocessing_options.active_processes,
      )
  )

  async def _load() -> Checkpointable:
    load_awaitable = await load_fn()
    blocking_end_time = time.time()
    event_tracking.OperationRecorder(
        path,
        operation_type=event_tracking.OperationType.LOAD,
        async_origin=False,
    ).record_blocking_completion(
        blocking_end_time - start_time,
        blocking_end_time,
    )
    result = await load_awaitable
    await multihost.sync_global_processes(
        multihost.unique_barrier_key(
            '_load_impl',
            prefix=ctx.multiprocessing_options.barrier_sync_key_prefix,
        ),
        operation_id=synchronization.get_operation_id(),
        processes=ctx.multiprocessing_options.active_processes,
    )
    return result

  result = asyncio_utils.run_sync(_load())

  duration_secs = time.time() - start_time
  event_tracking.OperationRecorder(
      path,
      operation_type=event_tracking.OperationType.LOAD,
      async_origin=False,
  ).record_completion(duration_secs)
  return result

