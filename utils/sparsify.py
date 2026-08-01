
def sparsify(f, use_tracer=False):
  """Experimental sparsification transform.

  Examples:

    Decorate JAX functions to make them compatible with :class:`jax.experimental.sparse.BCOO`
    matrices:

    >>> from jax.experimental import sparse

    >>> @sparse.sparsify
    ... def f(M, v):
    ...   return 2 * M.T @ v

    >>> M = sparse.BCOO.fromdense(jnp.arange(12).reshape(3, 4))

    >>> v = jnp.array([3, 4, 2])

    >>> f(M, v)
    Array([ 64,  82, 100, 118], dtype=int32)
  """
  if use_tracer:
    return _sparsify_with_tracer(f)
  else:
    return _sparsify_with_interpreter(f)

