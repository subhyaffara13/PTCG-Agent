
def key_reuse_error_with_source_traceback(
    message: str, traceback: source_info_util.Traceback | None) -> KeyReuseError:
  err = KeyReuseError(message)
  if traceback is not None:
    filtered_tb = traceback_util.filter_traceback(traceback.as_python_traceback())
    if filtered_tb:
      context_err = KeyReuseError(_source_context_message).with_traceback(filtered_tb)
      context_err.__context__ = err.__context__
      context_err.__cause__ = err.__cause__
      context_err.__suppress_context__ = err.__suppress_context__
      err.__context__ = None
      err.__cause__ = context_err
  return err

