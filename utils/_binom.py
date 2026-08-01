
def _binom(n, k):
  a = lax.lgamma(n + 1.0)
  b = lax.lgamma(n - k + 1.0)
  c = lax.lgamma(k + 1.0)
  return lax.exp(a - b - c)

