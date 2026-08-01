
def axis_size(axis_name: AxisName) -> int:
  """Return the size of the mapped axis ``axis_name``.

  Args:
    axis_name: hashable Python object used to name the mapped axis.

  Returns:
    An integer representing the size.

  For example, with 8 XLA devices available:

  >>> mesh = jax.make_mesh((8,), 'i')
  >>> @jax.shard_map(mesh=mesh, in_specs=jax.P('i'), out_specs=jax.P())
  ... def f(_):
  ...   return lax.axis_size('i')
  ...
  >>> f(jax.device_put(jnp.zeros(16), jax.NamedSharding(mesh, P('i'))))
  Array(8, dtype=int32, weak_type=True)

  >>> mesh = jax.make_mesh((4, 2), ('i', 'j'))
  >>> @jax.shard_map(mesh=mesh, in_specs=jax.P('i', 'j'), out_specs=jax.P())
  ... def f(_):
  ...   return lax.axis_size(('i', 'j'))
  ...
  >>> f(jax.device_put(jnp.zeros((16, 8)), jax.NamedSharding(mesh, P('i', 'j'))))
  Array(8, dtype=int32, weak_type=True)
  """
  return _axis_size(axis_name)

