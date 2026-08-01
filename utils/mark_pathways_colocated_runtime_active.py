
def mark_pathways_colocated_runtime_active() -> None:
  """Marks the current Python process as the Pathways colocated runtime."""
  multihost.mark_pathways_colocated_runtime_active()
  get_signaling_client.cache_clear()


def mark_pathways_colocated_runtime_active() -> None:
  """Marks the current Python process as the Pathways colocated runtime."""
  global _PATHWAYS_COLOCATED_RUNTIME_ACTIVE
  _PATHWAYS_COLOCATED_RUNTIME_ACTIVE = True

