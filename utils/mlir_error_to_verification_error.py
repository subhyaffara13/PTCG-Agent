
def mlir_error_to_verification_error(
    base_err: ir.MLIRError,
) -> VerificationError:
  """Reformats MLIRError to include a Python traceback."""
  diagnostic = base_err.error_diagnostics[0]
  def _get_diagnostic_message(diagnostic) -> str:
    current_msg = diagnostic.message
    for d in diagnostic.notes:
      current_msg += "\n " + _get_diagnostic_message(d)
    return current_msg

  _, frames = parse_location_string(str(diagnostic.location.attr))
  new_tb = traceback_from_raw_frames(frames)
  new_error = VerificationError(_get_diagnostic_message(diagnostic))
  new_error.__traceback__ = traceback_util.filter_traceback(new_tb)
  return new_error

