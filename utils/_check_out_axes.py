
def _check_out_axes(out_axes):
  for key, x in jax.tree_util.tree_leaves_with_path(
    out_axes, is_leaf=lambda x: x is None
  ):
    if x is None:
      raise ValueError(
        f'Cannot broadcast output state. '
        f'Got out_axes=None at: out_axes{jax.tree_util.keystr(key)}'
      )
    elif isinstance(x, StateAxes):
      for filter, value in x.items():
        if value is None:
          raise ValueError(
            f'Cannot broadcast output state. '
            f'Got StateAxes({{{filter}: None}}) at: out_axes'
            f'{jax.tree_util.keystr(key)}'
          )
        elif value is Carry:
          raise ValueError(
            f'Cannot carry output state. '
            f'Got StateAxes({{{filter}: Carry}}) at: out_axes'
            f'{jax.tree_util.keystr(key)}'
          )

