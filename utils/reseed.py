
def reseed(
  node,
  /,
  *,
  graph: bool | None = None,
  policy: tp.Literal['scalars_only', 'match_shape']
  | tp.Callable[
    [tuple, jax.Array, tuple[int, ...]], jax.Array
  ] = 'scalars_only',
  **stream_keys: RngValue,
):
  """Update the keys of the specified RNG streams with new keys.

  Args:
    node: the node to reseed the RNG streams in.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
    policy: defines how the new scalar key is for each RngStream is used to
      reseed the stream. If ``'scalars_only'`` is given (the default), an error is raised
      if the target stream key is not a scalar. If ``'match_shape'`` is given, the new
      scalar key is split to match the shape of the target stream key. A callable
      of the form ``(path, scalar_key, target_shape) -> new_key`` can be passed to
      define a custom reseeding policy.
    **stream_keys: a mapping of stream names to new keys. The keys can be
      either integers or ``jax.random.key``.

  Example::

    >>> from flax import nnx
    >>> import jax.numpy as jnp
    ...
    >>> class Model(nnx.Module):
    ...   def __init__(self, rngs):
    ...     self.linear = nnx.Linear(2, 3, rngs=rngs)
    ...     self.dropout = nnx.Dropout(0.5, rngs=rngs)
    ...   def __call__(self, x):
    ...     return self.dropout(self.linear(x))
    ...
    >>> model = Model(nnx.Rngs(params=0, dropout=42))
    >>> x = jnp.ones((1, 2))
    ...
    >>> y1 = model(x)
    ...
    >>> # reset the ``dropout`` stream key to 42
    >>> nnx.reseed(model, dropout=42)
    >>> y2 = model(x)
    ...
    >>> jnp.allclose(y1, y2)
    Array(True, dtype=bool)
  """
  if policy == 'scalars_only':
    policy = _scalars_only
  elif policy == 'match_shape':
    policy = _match_shape
  elif not callable(policy):
    raise ValueError(
      f'policy must be "scalars_only", "match_shape" or a callable, '
      f'got {policy!r}'
    )
  rngs = Rngs(**stream_keys)
  for path, stream in graphlib.iter_graph(node, graph=graph):
    if isinstance(stream, RngStream):
      if stream.key.tag in stream_keys:
        key = rngs[stream.key.tag]()
        key = policy(path, key, stream.key.shape)
        stream.key.set_value(key)
        stream.count.set_value(jnp.zeros(key.shape, dtype=jnp.uint32))

