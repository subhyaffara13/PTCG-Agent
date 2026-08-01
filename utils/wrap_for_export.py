
def wrap_for_export(f):
  """Wrap a function with error checking to make it compatible with AOT mode.

  Error checking relies on global state, which cannot be serialized across
  processes. This wrapper ensures that the error state remains within the
  function scope, making it possible to export the function and later import in
  other processes.

  When the function is later imported, it must be wrapped with
  :func:`unwrap_from_import` to integrate the error checking mechanism of the
  imported function into the global error checking mechanism of the current
  process.

  This function should only be applied once to a function; wrapping the same
  function multiple times is unnecessary.
  """

  def inner(*args, **kwargs):
    global _error_list

    # 1. Save the old state and initialize a new state.
    with core.eval_context():
      old_ref = _error_storage.ref
    _initialize_error_code_ref()
    with _error_list_lock:
      old_error_list, _error_list = _error_list, []

      # 2. Trace the function.
      out = f(*args, **kwargs)
      assert _error_storage.ref is not None
      error_code = _error_storage.ref[...].min()

      # 3. Restore the old state.
      _error_list, new_error_list = old_error_list, _error_list
    with core.eval_context():
      _error_storage.ref = old_ref

    new_error_list = [
        (msg, _traceback_to_str(traceback)) for msg, traceback in new_error_list
    ]
    return out, _ErrorClass(error_code, new_error_list)

  return inner

