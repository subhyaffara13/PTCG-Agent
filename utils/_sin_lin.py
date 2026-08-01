
def _sin_lin(_is_vjp, nzs, x, accuracy):
  nz, = nzs
  return (sin_p.bind(x, accuracy=accuracy), nz, cos(x),
          lambda cos_x, t: mul(t, cos_x))

