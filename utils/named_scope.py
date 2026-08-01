
def named_scope(
    name: str,
  ) -> source_info_util.ExtendNameStackContextManager:
  """A context manager that adds a user specified name to the JAX name stack.

  When staging out computations for just-in-time compilation to XLA (or other
  backends such as TensorFlow) JAX does not, by default, preserve the names
  (or other source metadata) of Python functions it encounters.
  This can make debugging the staged out (and/or compiled) representation of
  your program complicated because there is limited context information for each
  operation being executed.

  ``named_scope`` tells JAX to stage the given function with additional
  annotations on the underlying operations. JAX internally keeps track of these
  annotations in a name stack. When the staged out program is compiled with XLA
  these annotations are preserved and show up in debugging utilities like the
  TensorFlow Profiler in TensorBoard. Names are also preserved when staging out
  JAX programs to TensorFlow using :func:`experimental.jax2tf.convert`.


  Args:
    name: The prefix to use to name all operations created within the name
      scope.
  Yields:
    Yields ``None``, but enters a context in which `name` will be appended to
    the active name stack.

  Examples:
    ``named_scope`` can be used as a context manager inside compiled functions:

    >>> import jax
    >>>
    >>> @jax.jit
    ... def layer(w, x):
    ...   with jax.named_scope("dot_product"):
    ...     logits = w.dot(x)
    ...   with jax.named_scope("activation"):
    ...     return jax.nn.relu(logits)

    It can also be used as a decorator:

    >>> @jax.jit
    ... @jax.named_scope("layer")
    ... def layer(w, x):
    ...   logits = w.dot(x)
    ...   return jax.nn.relu(logits)
  """
  if not isinstance(name, str):
    raise TypeError("named_scope name argument must be a string.")
  return source_info_util.extend_name_stack(name)

