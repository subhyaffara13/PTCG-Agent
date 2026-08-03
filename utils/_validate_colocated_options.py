from typing import Any

def _validate_colocated_options(options: Any) -> None:
  """Rejects RCM options not yet supported by worker-side colocated MTC."""
  unsupported_options = [
      name
      for name in ('step_name_format', 'should_save_fn', 'preservation_policy')
      if getattr(options, name, None) is not None
  ]
  if unsupported_options:
    raise NotImplementedError(
        'Pathways colocated MTC does not support custom '
        'ReplicatorCheckpointManagerOptions for '
        f'{unsupported_options}.'
    )

