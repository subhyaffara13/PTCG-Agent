
def create_all_async(
    paths: Sequence[atomicity_types.TemporaryPath],
    completion_signals: Sequence[synchronization.HandlerAwaitableSignal],
    *,
    multiprocessing_options: options_lib.MultiprocessingOptions | None = None,
    subdirectories: Sequence[str] | None = None,
) -> future.Future:
  """Creates all temporary paths in parallel asynchronously.

  Args:
    paths: Sequence of temporary paths to create.
    completion_signals: Sequence of signals to send when all paths are created.
      Also adds them to the awaitable signals contract.
    multiprocessing_options: MultiprocessingOptions to use for barrier syncs and
      primary host.
    subdirectories: Sequence of subdirectories to create under `paths`. If not
      provided, no subdirectories will be created. The same set of
      subdirectories will be created under each path in `paths`.

  Returns:
    A future that which sends the completion signals when all paths are created.
  """
  multiprocessing_options = (
      multiprocessing_options or options_lib.MultiprocessingOptions()
  )
  barrier_sync_key_prefix = multiprocessing_options.barrier_sync_key_prefix
  active_processes = multiprocessing_options.active_processes
  primary_host = multiprocessing_options.primary_host
  # Sync for existence check to complete on all hosts before directory
  # creation starts.
  multihost.sync_global_processes(
      multihost.unique_barrier_key(
          'create_tmp_directory:post_existence_check',
          prefix=barrier_sync_key_prefix,
      ),
      timeout=multihost.coordination_timeout(),
      processes=active_processes,
  )

  commit_future = future.NoopFuture()
  if multihost.is_primary_host(primary_host):
    commit_future = future.CommitFutureAwaitingContractedSignals(
        _create_paths(
            paths,
            subdirectories=subdirectories,
        ),
        send_signals=completion_signals,
        timeout_secs=multihost.coordination_timeout(),
    )
    future.AwaitableSignalsContract.add_to_awaitable_signals_contract(
        completion_signals
    )

  # Sync to enusre that all hosts have the same awaitable signals contract.
  multihost.sync_global_processes(
      multihost.unique_barrier_key(
          'add_to_awaitable_signals_contract',
          prefix=barrier_sync_key_prefix,
      ),
      timeout=multihost.coordination_timeout(),
      processes=active_processes,
  )
  return commit_future

