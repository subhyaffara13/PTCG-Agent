
def _validate_colocated_python_runtime() -> None:
  """Validates that colocated Python MTC is only used on Pathways."""
  if not multihost.is_pathways_backend():
    raise ValueError(
        'Pathways colocated Python MTC requires a Pathways backend. '
        'McJAX MTC must use the standard ReplicatorCheckpointManager path '
        'with use_colocated_python=False.'
    )

