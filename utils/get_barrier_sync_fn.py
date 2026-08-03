import logging
from typing import Optional, Set

def get_barrier_sync_fn(
    *,
    processes: Optional[Set[int]] = None,
) -> BarrierSyncFn:
  """Provides a barrier synchronization function for JAX processes.

  Barriers with different sync keys are safe to use from independent background
  threads.

  Args:
    processes: If None, expects to wait across all processes and devices.
      Otherwise, creates a barrier only across devices associated with the given
      processes.

  Returns:
    A no-op function if there is a single JAX process, or
    A barrier synchronization callable which accepts two arguments: "key": [str]
    unique barrier id; "timeout_ms": [int] timeout to use for waiting on the
    barrier.
    Should be called from all JAX processes with the same sync key and will
    block until either 1) all processes have reached the barrier or
    2) the timeout is exceeded.
  """
  if should_skip_process_sync(processes):
    return lambda **kwargs: None

  client = get_jax_distributed_client()
  barrier_processes = processes or set(range(jax.process_count()))
  if process_index() not in barrier_processes:
    raise ValueError(
        'Attempted to create a barrier across a subset of processes, but the'
        f' current process: {process_index()} was not present in the provided'
        f' list of processes: {barrier_processes}.'
    )

  # Use distributed ids.
  if processes is None:
    barrier_processes = None
  else:
    # Don't map ids anymore if we are using distributed ids.
    barrier_processes = list(barrier_processes)

  def _fn(*, key: str, timeout_ms: int) -> None:
    key = _unique_barrier_key(key)
    logging.vlog(
        1,
        '[process=%s][thread=%s] Waiting at barrier: %s',
        process_index(),
        threading.current_thread().name,
        key,
    )
    if processes is None:
      client.wait_at_barrier(key, timeout_ms)
    else:
      logging.vlog(
          1,
          '[process=%s][thread=%s] Barrier processes: %s',
          process_index(),
          threading.current_thread().name,
          barrier_processes,
      )
      client.wait_at_barrier(key, timeout_ms, process_ids=barrier_processes)
    logging.vlog(
        1,
        '[process=%s][thread=%s] Done waiting at barrier: %s',
        process_index(),
        threading.current_thread().name,
        key,
    )

  return _fn

