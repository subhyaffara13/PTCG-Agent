
def disable_jit(disable: bool = True):
  """Context manager that disables :py:func:`jit` behavior under its dynamic context.

  For debugging, it is useful to have a mechanism that disables :py:func:`jit`
  everywhere in a dynamic context. Note that this not only disables explicit
  uses of :func:`jit` by the user, but will also remove any implicit JIT compilation
  used by the JAX library: this includes implicit JIT computation of `body` and
  `cond` functions passed to higher-level primitives like :func:`~jax.lax.scan` and
  :func:`~jax.lax.while_loop`, JIT used in implementations of :mod:`jax.numpy` functions,
  and any other case where :func:`jit` is used within an API's implementation.
  Note however that even under `disable_jit`, individual primitive operations
  will still be compiled by XLA as in normal eager op-by-op execution.

  Values that have a data dependence on the arguments to a jitted function are
  traced and abstracted. For example, an abstract value may be a
  :py:class:`ShapedArray` instance, representing the set of all possible arrays
  with a given shape and dtype, but not representing one concrete array with
  specific values. You might notice those if you use a benign side-effecting
  operation in a jitted function, like a print:

  >>> import jax
  >>>
  >>> @jax.jit
  ... def f(x):
  ...   y = x * 2
  ...   print("Value of y is", y)
  ...   return y + 3
  ...
  >>> print(f(jax.numpy.array([1, 2, 3])))
  Value of y is JitTracer(int32[3])
  [5 7 9]

  Here ``y`` has been abstracted by :py:func:`jit` to a :py:class:`ShapedArray`,
  which represents an array with a fixed shape and type but an arbitrary value.
  The value of ``y`` is also traced. If we want to see a concrete value while
  debugging, and avoid the tracer too, we can use the :py:func:`disable_jit`
  context manager:

  >>> import jax
  >>>
  >>> with jax.disable_jit():
  ...   print(f(jax.numpy.array([1, 2, 3])))
  ...
  Value of y is [2 4 6]
  [5 7 9]
  """
  with config.disable_jit(disable):
    yield

