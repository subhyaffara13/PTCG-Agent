
def _layout_constraint_impl(x, *, layout):
  if not isinstance(x, xc.ArrayImpl):
    raise ValueError(
        'with_layout_constraint in eager mode can only be applied to'
        f' jax.Arrays. Got {type(x)}')
  if x.format.layout == layout:
    return x
  return api.jit(_identity_fn, out_shardings=Format(layout, x.sharding))(x)

