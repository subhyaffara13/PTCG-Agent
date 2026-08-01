
def reached_preemption(step: int) -> bool:
  """Returns True if a preemption sync point has been reached."""
  # TODO(b/403305420) : disable checkpoing saving when preemption for MLCR.
  # Remove this once the bug is closed.
  if is_proxy_pathways_backend():
    return False

  preemption_sync_point_reached = multihost_utils.reached_preemption_sync_point(
      step
  )
  _maybe_log_reached_preemption(step, preemption_sync_point_reached)
  return preemption_sync_point_reached

