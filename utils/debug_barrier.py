
def debug_barrier() -> None:
  """Synchronizes all kernel executions in the grid."""
  return debug_barrier_p.bind()

