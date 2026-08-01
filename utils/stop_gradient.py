
def stop_gradient(x: T) -> T:
  """Stops gradient computation.

  Operationally ``stop_gradient`` is the identity function, that is, it returns
  argument `x` unchanged. However, ``stop_gradient`` prevents the flow of
  gradients during forward or reverse-mode automatic differentiation. If there
  are multiple nested gradient computations, ``stop_gradient`` stops gradients
  for all of them. For some discussion of where this is useful, refer to
  :ref:`stopping-gradients`.

  Args:
    x: array or pytree of arrays

  Returns:
    input value is returned unchanged, but within autodiff will be treated as
    a constant.

  Examples:
    Consider a simple function that returns the square of the input value:

    >>> def f1(x):
    ...   return x ** 2
    >>> x = jnp.float32(3.0)
    >>> f1(x)
    Array(9.0, dtype=float32)
    >>> jax.grad(f1)(x)
    Array(6.0, dtype=float32)

    The same function with ``stop_gradient`` around ``x`` will be equivalent
    under normal evaluation, but return a zero gradient because ``x`` is
    effectively treated as a constant:

    >>> def f2(x):
    ...   return jax.lax.stop_gradient(x) ** 2
    >>> f2(x)
    Array(9.0, dtype=float32)
    >>> jax.grad(f2)(x)
    Array(0.0, dtype=float32)

    This is used in a number of places within the JAX codebase; for example
    :func:`jax.nn.softmax` internally normalizes the input by its maximum
    value, and this maximum value is wrapped in ``stop_gradient`` for
    efficiency. Refer to :ref:`stopping-gradients` for more discussion of
    the applicability of ``stop_gradient``.
  """
  return tree_util.tree_map(_stop_gradient, x)

