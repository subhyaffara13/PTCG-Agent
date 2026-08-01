
def _zeta_series_expansion(x: ArrayLike, q: ArrayLike | None = None) -> Array:
  if q is None:
    raise NotImplementedError(
      "Riemann zeta function not implemented; pass q != None to compute the Hurwitz Zeta function.")
  # Reference: Johansson, Fredrik.
  # "Rigorous high-precision computation of the Hurwitz zeta function and its derivatives."
  # Numerical Algorithms 69.2 (2015): 253-270.
  # https://arxiv.org/abs/1309.2877 - formula (5)
  # here we keep the same notation as in reference
  s, a = promote_args_inexact("zeta", x, q)
  dtype = lax.dtype(a).type
  s_, a_ = jnp.expand_dims(s, -1), jnp.expand_dims(a, -1)
  # precision ~ N, M
  N = M = dtype(8) if lax.dtype(a) == np.float32 else dtype(16)
  assert M <= len(_BERNOULLI_COEFS)
  k = jnp.expand_dims(np.arange(N, dtype=N.dtype), tuple(range(a.ndim)))
  S = jnp.sum((a_ + k) ** -s_, -1)
  I = lax.div((a + N) ** (dtype(1) - s), s - dtype(1))
  T0 = (a + N) ** -s
  m = jnp.expand_dims(np.arange(2 * M, dtype=M.dtype), tuple(range(s.ndim)))
  s_over_a = (s_ + m) / (a_ + N)
  T1 = jnp.cumprod(s_over_a, -1)[..., ::2]
  T1 = jnp.clip(T1, max=dtypes.finfo(dtype).max)
  coefs = np.expand_dims(np.array(_BERNOULLI_COEFS[:T1.shape[-1]], dtype=dtype),
                         tuple(range(a.ndim)))
  T1 = T1 / coefs
  T = T0 * (dtype(0.5) + T1.sum(-1))
  return S + I + T

