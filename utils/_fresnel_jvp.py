
def _fresnel_jvp(primals, tangents):
  x, = primals
  x_dot, = tangents
  result = fresnel(x)
  sinpi, cospi = sincospisquaredhalf(x)
  dSdx = sinpi * x_dot
  dCdx = cospi * x_dot
  return result, (dSdx, dCdx)

