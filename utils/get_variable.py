
def get_variable(type_var: str):
  """Get a variable of various shape."""
  if type_var == 'real_array':
    return jnp.asarray([1.0, 2.0])
  if type_var == 'complex_array':
    return jnp.asarray([1.0 + 1j * 2.0, 3.0 + 4j * 5.0])
  if type_var == 'pytree':
    pytree = {'k1': 1.0, 'k2': (2.0, 3.0), 'k3': jnp.asarray([4.0, 5.0])}
    return jax.tree.map(jnp.asarray, pytree)
  raise ValueError(f'Invalid type_var {type_var}')

