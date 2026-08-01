
def _maybe_log_reached_preemption(
    step: int, preemption_sync_point_reached: bool
):
  if not preemption_sync_point_reached:
    return
  jax.monitoring.record_event('/jax/orbax/write/preemption')
  logging.warning(
      '[process=%s][thread=%s] Reached preemption sync point, step=%s',
      process_index(),
      threading.current_thread().name,
      step,
  )

