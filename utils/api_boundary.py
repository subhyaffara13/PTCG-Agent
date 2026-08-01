
def api_boundary(
    fun: C, *,
    repro_api_name: str | None = None,
    repro_user_func: bool = False) -> C:
  '''Wraps ``fun`` to form a boundary for filtering exception tracebacks.

  When an exception occurs below ``fun``, this appends to it a custom
  ``__cause__`` that carries a filtered traceback. The traceback imitates the
  stack trace of the original exception, but with JAX-internal frames removed.

  This boundary annotation works in composition with itself. The topmost frame
  corresponding to an :func:`~api_boundary` is the one below which stack traces
  are filtered. In other words, if ``api_boundary(f)`` calls
  ``api_boundary(g)``, directly or indirectly, the filtered stack trace provided
  is the same as if ``api_boundary(f)`` were to simply call ``g`` instead.

  This annotation is primarily useful in wrapping functions output by JAX's
  transformations. For example, consider ``g = jax.jit(f)``. When ``g`` is
  called, JAX's JIT compilation machinery is invoked, which in turn calls ``f``
  in order to trace and translate it. If the function ``f`` raises an exception,
  the stack unwinds through JAX's JIT internals up to the original call site of
  ``g``. Because the function returned by :func:`~jax.jit` is annotated as an
  :func:`~api_boundary`, such an exception is accompanied by an additional
  traceback that excludes the frames specific to JAX's implementation.

  For the "repro" kwargs, see the comments for `repro.boundary`.
  '''

  @functools.wraps(fun)  # pyrefly: ignore[bad-argument-type]
  def reraise_with_filtered_traceback(*args, **kwargs):
    __tracebackhide__ = True
    try:
      return fun(*args, **kwargs)  # pyrefly: ignore[not-callable]
    except Exception as e:
      mode = _filtering_mode()
      if _is_under_reraiser(e) or mode == "off":
        raise
      if mode == "tracebackhide":
        _add_tracebackhide_to_hidden_frames(e.__traceback__)
        raise

      tb = e.__traceback__
      if tb is None:
        raise TypeError("Traceback is None") from e
      try:
        e.with_traceback(filter_traceback(tb))
        if mode == "quiet_remove_frames":
          e.add_note("--------------------\n" + _simplified_tb_msg)
        else:
          if mode == "remove_frames":
            msg = format_exception_only(e)
            msg = f'{msg}\n\n{_jax_message_append}'
            jax_error = UnfilteredStackTrace(msg)
            jax_error.with_traceback(_add_call_stack_frames(tb))
          else:
            raise ValueError(f"JAX_TRACEBACK_FILTERING={mode} is not a valid value.")
          jax_error.__cause__ = e.__cause__
          jax_error.__context__ = e.__context__
          jax_error.__suppress_context__ = e.__suppress_context__
          e.__cause__ = jax_error
          e.__context__ = None
          del jax_error
        raise
      finally:
        del mode, tb
  if repro and (repro_api_name or repro_user_func):
    reraise_with_filtered_traceback = repro.boundary(
        reraise_with_filtered_traceback, api_name=repro_api_name,
        is_user=repro_user_func)
  return cast(C, reraise_with_filtered_traceback)

