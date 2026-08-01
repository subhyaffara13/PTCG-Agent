
def _handle_xla_runtime_error(
    base_err: _jax.JaxRuntimeError,
) -> MosaicError | None:
  """Reformats JaxRuntimeError to include a Python traceback."""
  if 'Mosaic' not in str(base_err):
    return None
  try:
    _, frames = parse_location_string(str(base_err))
  except ValueError:
    # If no location string is found, skip handling and raise the original
    # error.
    return None
  new_tb = traceback_from_raw_frames(frames)
  err_msg = base_err.args[0]
  err_msg = redact_locations(err_msg)
  new_error = MosaicError(err_msg)
  new_error.__traceback__ = traceback_util.filter_traceback(new_tb)
  return new_error

