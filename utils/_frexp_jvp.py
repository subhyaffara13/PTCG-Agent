
def _frexp_jvp(primals, tangents):
  x, = primals
  t, = tangents
  m, e = frexp(x)
  mdot = t * exp2(-e.astype(t.dtype))
  edot = lax.full_like(e, fill_value=0, dtype=dtypes.float0)
  return (m, e), (mdot, edot)

