
def unwrap_from_import(f):
  """Unwrap a function after AOT import to restore error checking.

  When an AOT-exported function is imported in a new process, its error state is
  separate from the global error state of the current process. This wrapper
  ensures that errors detected during execution are correctly integrated into
  the global error checking mechanism of the current process.

  This function should only be applied to functions that were previously wrapped
  with :func:`wrap_for_export` before export.
  """
  if _error_storage.ref is None:
    with core.eval_context():
      _initialize_error_code_ref()
    assert _error_storage.ref is not None

  def inner(*args, **kwargs):
    out, error_class = f(*args, **kwargs)
    new_error_code, error_list = error_class.error_code, error_class.error_list

    # Update the global error list.
    with _error_list_lock:
      offset = len(_error_list)
      _error_list.extend(error_list)

    # Update the global error code array.
    assert _error_storage.ref is not None
    error_code = _error_storage.ref[...]
    should_update = lax.bitwise_and(
        error_code == np.uint32(_NO_ERROR),
        new_error_code != np.uint32(_NO_ERROR),
    )
    error_code = lax.select(should_update, new_error_code + offset, error_code)

    # TODO(ayx): support vmap and shard_map.
    _error_storage.ref[...] = error_code

    return out

  return inner

