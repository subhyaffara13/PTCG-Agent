
def expn_jvp(n, primals, tangents):
  (x,), (x_dot,) = primals, tangents
  return expn(n, x), lax.mul(
    lax.neg(x_dot), expn(lax.sub(n, _lax_const(n, 1)), x)
  )

