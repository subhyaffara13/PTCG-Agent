
def _background_wait_for_commit_futures(
    directory: epath.Path,
    commit_futures: Sequence[future.Future],
    on_commit_callback: Callable[[], None],
    *,
    barrier_sync_key_prefix: str,
    sync_fn: Callable[[str, int], None],
    timeout_secs: int,
    primary_host: int | None,
):
  """A function to be run in a background thread that waits for futures."""
  current_process = multihost.process_index()
  current_thread_id = threading.current_thread().name
  process_count = jax.process_count()
  logging.info(
      '[process=%s][thread=%s] Background save thread started. Deadline for'
      ' this save operation is %s',
      current_process,
      current_thread_id,
      datetime.datetime.now() + datetime.timedelta(seconds=timeout_secs),
  )
  thread_start_time = time.time()

  # Wait for commit operations to complete.
  future.ChainedFuture(commit_futures, cb=lambda: None).result(
      timeout=timeout_secs
  )
  commit_duration_secs = time.time() - thread_start_time
  logging.info(
      '[process=%s][thread=%s] %d Handler Commit operations completed. Time'
      ' taken: %fs.',
      current_process,
      current_thread_id,
      len(commit_futures),
      commit_duration_secs,
  )
  jax.monitoring.record_scalar(
      '/jax/checkpoint/write/async/commit_future_count',
      len(commit_futures),
  )
  # Log the per process storage commit latency excluding the barrier time.
  jax.monitoring.record_event_duration_secs(
      '/jax/checkpoint/write/async/commit_duration_sec',
      commit_duration_secs,
  )

  if process_count > 1:
    # All processes will wait at the barrier. When all processes are at the
    # barrier, the barrier will be satisfied. If not, then it will timeout.
    try:
      time_remaining_secs = future.get_remaining_time(
          thread_start_time, timeout_secs
      )
      sync_fn(
          multihost.unique_barrier_key(
              'async_write_complete',
              prefix=barrier_sync_key_prefix,
              suffix=f'{directory.name}',
          ),
          int(time_remaining_secs * 1000),
      )
    except jax.errors.JaxRuntimeError as e:
      if sys.version_info >= (3, 11):
        if 'DEADLINE_EXCEEDED' in str(e):
          _add_deadline_exceeded_notes(e)
      raise TimeoutError(
          'Timed out while waiting for async_write_complete barrier.'
      ) from e

  if utils.is_primary_host(primary_host):
    on_commit_callback()
  if process_count > 1:
    # Block until process 0 completes on_commit_callback.
    try:
      time_remaining_secs = future.get_remaining_time(
          thread_start_time, timeout_secs
      )
      sync_fn(
          multihost.unique_barrier_key(
              'async_commit_complete',
              prefix=barrier_sync_key_prefix,
              suffix=f'{directory.name}',
          ),
          int(time_remaining_secs * 1000),
      )
    except jax.errors.JaxRuntimeError as e:
      if sys.version_info >= (3, 11):
        if 'DEADLINE_EXCEEDED' in str(e):
          _add_deadline_exceeded_notes(e)
      raise TimeoutError(
          'Timed out while waiting for async_commit_complete barrier.'
      ) from e

  thread_duration_secs = time.time() - thread_start_time
  jax.monitoring.record_event_duration_secs(
      '/jax/checkpoint/write/async/thread_duration_sec',
      thread_duration_secs,
  )
  logging.info(
      '[process=%s][thread=%s] Background save thread done. Time taken: %fs.',
      current_process,
      current_thread_id,
      thread_duration_secs,
  )

