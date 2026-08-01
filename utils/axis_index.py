
def axis_index(axis_name: AxisName) -> Array:
  """Return the index along the mapped axis ``axis_name``.

  Args:
    axis_name: hashable Python object used to name the mapped axis.

  Returns:
    An integer representing the index.

  For example, with 8 XLA devices available:

  >>> mesh = jax.make_mesh((8,), 'i')
  >>> @jax.shard_map(mesh=mesh, in_specs=(), out_specs=jax.P('i'))
  ... def f():
  ...   return lax.axis_index('i')[None]
  ...
  >>> f()
  Array([0, 1, 2, 3, 4, 5, 6, 7], dtype=int32)

  >>> mesh = jax.make_mesh((4, 2), ('i', 'j'))
  >>> @jax.shard_map(mesh=mesh, in_specs=(), out_specs=jax.P('i', 'j'))
  ... def f():
  ...   return lax.axis_index(('i', 'j'))[None, None]
  ...
  >>> f()
  Array([[0, 1],
         [2, 3],
         [4, 5],
         [6, 7]], dtype=int32)
  """
  if not isinstance(axis_name, (tuple, list)):
    return axis_index_p.bind(axis_name=axis_name)
  else:
    inner_size = 1
    index = lax.asarray(0)
    for name in reversed(axis_name):
      index += axis_index(name) * inner_size
      inner_size *= axis_size(name)
    return index

