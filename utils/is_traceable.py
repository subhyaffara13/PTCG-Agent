
def is_traceable(fn) -> bool:
  """Checks if function is traceable.

  JAX traces a function when it is wrapped with @jit, @pmap, or @vmap.
  In other words, this function checks whether `fn` is wrapped with any of
  the aforementioned JAX transformations.

  Args:
    fn: function to assert.

  Returns:
    Bool indicating whether fn is traceable.
  """

  fn_string_tokens = (
      ".reraise_with_filtered_traceback",  # JIT    in Python ver. >= 3.7
      "CompiledFunction",  # C++ JIT in jaxlib 0.1.66 or newer.
      "pmap.",  # Python pmap
      "PmapFunction",  # C++ pmap in jaxlib 0.1.72 or newer.
      "vmap.",  # vmap
      "_python_pjit",
      "_cpp_pjit",
  )

  fn_type_tokens = (
      "PmapFunction",
      "PjitFunction",
  )

  # Un-wrap `fn` and check if any internal fn is jitted by pattern matching.
  fn_ = fn
  while True:
    if any(t in str(fn_) for t in fn_string_tokens):
      return True

    if any(t in str(type(fn_)) for t in fn_type_tokens):
      return True

    if hasattr(fn_, "__wrapped__"):
      # Wrapper.
      fn_globals = getattr(fn_, "__globals__", {})

      if fn_globals.get("__name__", None) == "jax.api":
        # Wrapper from `jax.api`.
        return True

      if "api_boundary" in fn_globals:
        # api_boundary is a JAX wrapper for traced functions.
        return True

    else:
      break

    fn_ = fn_.__wrapped__
  return False

