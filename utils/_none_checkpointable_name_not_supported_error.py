from pathlib import Path


def _none_checkpointable_name_not_supported_error(
    path: Path,
) -> ValueError:
  return ValueError(
      f"Attempting to load V1 checkpoint at {path} with"
      " `checkpointable_name=None`. This is only supported for legacy V0"
      " checkpoints. Please specify the name of the checkpointable to load."
      " Otherwise, omit `checkpointable_name` to load default 'pytree'"
      " checkpointable."
  )

