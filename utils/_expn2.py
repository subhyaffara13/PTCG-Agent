
def _expn2(x: Array, n: Array) -> Array:
  # x > 1.
  _c = _lax_const
  BIG = _c(x, 1.44115188075855872e17)
  MACHEP = dtypes.finfo(x.dtype).eps
  zero = _c(x, 0.0)
  one = _c(x, 1.0)

  init = dict(
    k=_c(n, 1),
    pkm2=one,
    qkm2=x,
    pkm1=one,
    qkm1=x + n,
    ans=one / (x + n),
    t=_c(x, np.inf),
    r=zero,
    x=x,
  )

  def body(d):
    x = d["x"]
    d["k"] += _c(d["k"], 1)
    k = d["k"]
    odd = k % _c(k, 2) == _c(k, 1)
    yk = jnp.where(odd, one, x)
    xk = jnp.where(odd, n + (k - _c(k, 1)) / _c(k, 2), k / _c(k, 2))
    pk = d["pkm1"] * yk + d["pkm2"] * xk
    qk = d["qkm1"] * yk + d["qkm2"] * xk
    nz = qk != zero
    d["r"] = r = jnp.where(nz, pk / qk, d["r"])
    d["t"] = jnp.where(nz, abs((d["ans"] - r) / r), one)
    d["ans"] = jnp.where(nz, r, d["ans"])
    d["pkm2"] = d["pkm1"]
    d["pkm1"] = pk
    d["qkm2"] = d["qkm1"]
    d["qkm1"] = qk
    is_big = abs(pk) > BIG
    for s in "pq":
      for i in "12":
        key = s + "km" + i
        d[key] = jnp.where(is_big, d[key] / BIG, d[key])
    return d

  def cond(d):
    return (d["x"] > _c(d["k"], 0)) & (d["t"] > MACHEP)

  d = lax.while_loop(cond, body, init)
  return d["ans"] * jnp.exp(-x)

