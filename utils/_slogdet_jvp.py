
def _slogdet_jvp(primals, tangents):
  """JVP for (sign, logabsdet). Uses d/dA log|det(A)| = trace(A⁻¹ Ȧ); sign_dot
  is zero for real (sign is not differentiable at 0) and set per complex case."""
  x, = primals
  g, = tangents
  sign, ans = slogdet(x)
  ans_dot = jnp.trace(solve(x, g), axis1=-1, axis2=-2)
  if jnp.issubdtype(jnp._dtype(x), np.complexfloating):
    sign_dot = (ans_dot - ufuncs.real(ans_dot).astype(ans_dot.dtype)) * sign
    ans_dot = ufuncs.real(ans_dot)
  else:
    sign_dot = array_creation.zeros_like(sign)
  return (sign, ans), (sign_dot, ans_dot)

