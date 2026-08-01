
def raise_if_error() -> None:
  """Raise an exception if the internal error state is set.

  This function should be called after a computation completes to check for any
  errors that were marked during execution via `set_error_if()`. If an error
  exists, it raises a `JaxValueError` with the corresponding error message.

  This function should not be called inside a traced function (e.g., inside
  :func:`jax.jit`). Doing so will raise a `ValueError`.

  Raises:
    JaxValueError: If the internal error state is set.
    ValueError: If called within a traced JAX function.
  """
  if _error_storage.ref is None:  # if not initialized, do nothing
    return

  error_code = _error_storage.ref[...].min()  # reduce to a single error code
  if isinstance(error_code, core.Tracer):
    raise ValueError(
        "raise_if_error() should not be called within a traced context, such as"
        " within a jitted function."
    )
  if error_code == np.uint32(_NO_ERROR):
    return
  _error_storage.ref[...] = lax.full(
      _error_storage.ref.shape,
      np.uint32(_NO_ERROR),
      sharding=_error_storage.ref.sharding,
  )  # clear the error code

  with _error_list_lock:
    if error_code < 0 or error_code >= len(_error_list):
      # Handle invalid error codes gracefully with a standard error message.
      # This can happen with corrupted AOT serialization data or negative
      # error codes that could lead to incorrect indexing.
      msg, traceback = _INVALID_ERROR_CODE_MSG, _INVALID_ERROR_CODE_TRACEBACK
    else:
      msg, traceback = _error_list[error_code]
  if isinstance(traceback, str):  # from imported AOT functions
    exc = JaxValueError(
        f"{msg}\nThe original traceback is shown below:\n{traceback}"
    )
    raise exc
  else:
    exc = JaxValueError(msg)
    raise exc.with_traceback(traceback)

