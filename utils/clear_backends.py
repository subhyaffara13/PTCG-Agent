
def clear_backends(domain, registered=True, globals=False):
    """
    This utility method clears registered backends.

    .. warning::
        We caution library authors against using this function in
        their code. We do *not* support this use-case. This function
        is meant to be used only by users themselves.

    .. warning::
        Do NOT use this method inside a multimethod call, or the
        program is likely to crash.

    Parameters
    ----------
    domain : Optional[str]
        The domain for which to de-register backends. ``None`` means
        de-register for all domains.
    registered : bool
        Whether or not to clear registered backends. See :obj:`register_backend`.
    globals : bool
        Whether or not to clear global backends. See :obj:`set_global_backend`.

    See Also
    --------
    register_backend : Register a backend globally.
    set_global_backend : Set a global backend.
    """
    _uarray.clear_backends(domain, registered, globals)


def clear_backends(_crash=False):
  """
  Clear all backend clients so that new backend clients can be created later.
  """
  clients = []
  if config.debug_leaked_clients_on_clear_backends.value:
    try:
      if xb.backends_are_initialized():
        clients = [weakref.ref(c) for c in xb._backends.values()]
    except Exception:
      pass

  effects_barrier()
  xb._clear_backends()
  util.clear_all_caches()
  pjit._cpp_pjit_cache_fun_only.clear()
  pjit._cpp_pjit_cache_explicit_attributes.clear()
  _jax.PjitFunctionCache.clear_all()

  if clients:
    # GC a couple times because there are false cycles that seem to be due
    # to captured stack traces in exceptions raised during testing.
    # TODO(parkers): Figure out how to make this a single gc.collect() call.
    for _ in range(4):
      gc.collect()
    for r in clients:
      if r() is not None:
        if _crash:
          print("A jax.Client was leaked", file=sys.stderr)
          os._exit(-1)
        else:
          raise RuntimeError("A jax.Client was leaked")

