
def _expn1(x: Array, n: Array) -> Array:
  # exponential integral En
  _c = _lax_const
  MACHEP = dtypes.finfo(x.dtype).eps

  zero = _c(x, 0.0)
  one = _c(x, 1.0)
  psi = -np.euler_gamma - jnp.log(x)
  psi = lax.fori_loop(_c(n, 1), n, lambda i, psi: psi + one / i, psi)
  n1 = jnp.where(n == _c(n, 1), one + one, n)
  init = dict(
    x=x,
    z=-x,
    xk=zero,
    yk=one,
    pk=one - n,
    ans=jnp.where(n == _c(n, 1), zero, one / (one - n1)),
    t=np.inf,
  )

  def body(d):
    d["xk"] += one
    d["yk"] *= d["z"] / d["xk"]
    d["pk"] += one
    d["ans"] += jnp.where(d["pk"] != zero, d["yk"] / d["pk"], zero)
    d["t"] = jnp.where(d["ans"] != zero, abs(d["yk"] / d["ans"]), one)
    return d

  def cond(d):
    return (d["x"] > _c(d["x"], 0.0)) & (d["t"] > MACHEP)

  d = lax.while_loop(cond, body, init)
  t = n
  r = n - _c(n, 1)
  return d["z"] ** r * psi / jnp.exp(gammaln(t)) - d["ans"]

