
def sync_global_processes(name: str):
  multihost_utils.sync_global_devices(name)


def sync_global_processes(
    name: str,
    *,
    timeout: Optional[int] = None,
    processes: Optional[Set[int]] = None,
    barrier_sync_fn: Optional[BarrierSyncFn] = None,
    record_event_name: str = '/jax/checkpoint/sync_global_devices_duration_sec',
):
  """Barrier to sync concurrent processes.

  NOTE: The barrier name must be unique, i.e. no process should wait on the
  same barrier name multiple times.

  Args:
    name: barrier name. Must be unique.
    timeout: timeout in seconds.
    processes: If None, expects to wait across all processes and devices.
      Otherwise, creates a barrier only across devices associated with the given
      processes.
    barrier_sync_fn: Used as the implementation for the synchronization. If not
      provided, a default implementation is used.
    record_event_name: The name of the event to record the duration of the
      synchronization.
  """
  if should_skip_process_sync(processes):
    logging.vlog(
        1,
        '[process=%s][thread=%s] Skipping global process sync, barrier'
        ' name: %s',
        process_index(),
        threading.current_thread().name,
        name,
    )
    return
  timeout = timeout or _DEFAULT_BARRIER_TIMEOUT
  sync_start_time = time.time()
  try:
    use_distributed_barrier = EXPERIMENTAL_ORBAX_USE_DISTRIBUTED_BARRIER.value
  except Exception:  # pylint: disable=broad-exception-caught
    logging.log_first_n(
        logging.INFO,
        '[thread=%s] Failed to get flag value for'
        ' EXPERIMENTAL_ORBAX_USE_DISTRIBUTED_BARRIER.',
        1,
        threading.current_thread().name,
    )
    use_distributed_barrier = False

  # Temporarily default to existing behavior to minimize risk of breakage.
  if processes is None and not use_distributed_barrier:
    key = _unique_barrier_key(name)
    logging.vlog(
        1,
        '[process=%s][thread=%s] Begin jax/sync_global_devices("%s")',
        process_index(),
        threading.current_thread().name,
        key,
    )
    multihost_utils.sync_global_devices(key)
    logging.vlog(
        1,
        '[process=%s][thread=%s] Done jax/sync_global_devices("%s"): %s secs',
        process_index(),
        threading.current_thread().name,
        key,
        (time.time() - sync_start_time),
    )
  else:
    barrier_sync_fn = barrier_sync_fn or get_barrier_sync_fn(
        processes=processes
    )
    barrier_sync_fn(key=name, timeout_ms=timeout * 1000)
  # This may end up just being too noisy given how many barriers there are, but
  # it does represent how long different processes waited around waiting for
  # other processes to reach a barrier.
  jax.monitoring.record_event_duration_secs(
      record_event_name,
      time.time() - sync_start_time,
  )


def sync_global_processes(
    name: str,
) -> None:
  """Syncs global processes using torch if available, else multihost."""
  try:
    import torch.distributed as dist  # pylint: disable=g-import-not-at-top

    if dist.is_initialized():
      logging.vlog(
          1,
          "[process=%s][thread=%s] sync_global_processes with torch"
          " barrier: %s",
          dist.get_rank(),
          threading.current_thread().name,
          name,
      )
      dist.barrier()
      return
  except ImportError:
    pass
  multihost.sync_global_processes(name)

