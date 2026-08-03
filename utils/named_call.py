import functools

def named_call(
    fun: F,
    *,
    name: str | None = None,
) -> F:
  """Adds a user specified name to a function when staging out JAX computations.

  When staging out computations for just-in-time compilation to XLA (or other
  backends such as TensorFlow) JAX runs your Python program but by default does
  not preserve any of the function names or other metadata associated with it.
  This can make debugging the staged out (and/or compiled) representation of
  your program complicated because there is limited context information for each
  operation being executed.

  `named_call` tells JAX to stage the given function out as a subcomputation
  with a specific name. When the staged out program is compiled with XLA these
  named subcomputations are preserved and show up in debugging utilities like
  the TensorFlow Profiler in TensorBoard. Names are also preserved when staging
  out JAX programs to TensorFlow using :func:`experimental.jax2tf.convert`.

  Args:
    fun: Function to be wrapped. This can be any Callable.
    name: Optional. The prefix to use to name all sub computations created
      within the name scope. Use the fun.__name__ if not specified.

  Returns:
    A version of ``fun`` that is wrapped in a ``named_scope``.
  """
  if name is None:
    name = fun.__name__

  return source_info_util.extend_name_stack(name)(fun)


def named_call(class_fn, force=True):
  """Labels a method for labelled traces in profiles.

  Note that it is better to use the `jax.named_scope` context manager directly
  to add names to JAX's metadata name stack.

  Args:
    class_fn: The class method to label.
    force: If True, the named_call transform is applied even if it is globally
      disabled. (e.g.: by calling `flax.linen.disable_named_call()`)
  Returns:
    A wrapped version of ``class_fn`` that is labeled.
  """

  # We use JAX's dynamic name-stack named_call. No transform boundary needed!
  @functools.wraps(class_fn)
  def wrapped_fn(self, *args, **kwargs):
    if (not force and not linen_module._use_named_call) or self._state.in_setup:  # pylint: disable=protected-access  # pylint: disable=protected-access
      return class_fn(self, *args, **kwargs)
    full_name = _derive_profiling_name(self, class_fn)
    return jax.named_call(class_fn, name=full_name)(self, *args, **kwargs)

  return wrapped_fn

