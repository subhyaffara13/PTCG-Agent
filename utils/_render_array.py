
def _render_array(x):
  shape, dtype = jnp.shape(x), jnp.result_type(x)
  shape_repr = ','.join(str(x) for x in shape)
  return f'[dim]{dtype}[/dim][{shape_repr}]'

