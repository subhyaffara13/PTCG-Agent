
def _reduce_or_lin(_is_vjp, nzs, x, *, axes):
  nz, = nzs
  y = reduce_or_p.bind(x, axes=axes)
  aval = typeof(y).to_tangent_aval()
  return y, False, (), lambda _, t: ad_util.Zero(aval)

