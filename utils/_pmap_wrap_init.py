
def _pmap_wrap_init(f, static_broadcasted_tuple):
  """Create a wrapped function with DebugInfo for pmap.

  Args:
    f: The function to wrap.
    static_broadcasted_tuple: Tuple of static argument indices.

  Returns:
    A lu.WrappedFun ready for pmap.
  """
  # Compute arg_names from signature, excluding static argnums
  if (signature := fun_signature(f)) is not None:
    static_set = frozenset(static_broadcasted_tuple)
    arg_names = tuple(
        name
        for i, name in enumerate(signature.parameters.keys())
        if i not in static_set
    )
  else:
    arg_names = None
  dbg = lu.DebugInfo("pmap", fun_sourceinfo(f), arg_names, None)
  return lu.wrap_init(f, debug_info=dbg)

