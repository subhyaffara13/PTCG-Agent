
def _check_data_iter(value: Any):
  """Checks if data_iter is valid."""
  if utils.pygrain() is None:
    raise ImportError(
        'grain library is not available. Please install grain to use data_iter.'
    )
  if not isinstance(
      value,
      (
          utils.pygrain().PyGrainCheckpointSave,
          utils.pygrain().PyGrainCheckpointRestore,
      ),
  ):
    raise TypeError(f'Unsupported type for data_iter: {type(value)}')

