
def _fiedler_companion(a: Array) -> Array:
  n = a.shape[0] - 1
  if n == 0:
    return jnp.empty_like(a, shape=(0, 0))
  a = a / a[0]
  if n == 1:
    return -a[1:].reshape(1, 1)
  # Build the matrix with full-grid masked assignments so static shapes are
  # preserved under jit and vectorize. The pentadiagonal layout is:
  #   c[0, 0]               = -a[1]            (first column top)
  #   c[1, 0]               = 1                (first column second row)
  #   c[i,   i+1]           = -a[i+2]          (super-diag, even i, i+1 < n)
  #   c[i,   i+2]           = 1                (second super, even i, i+2 < n)
  #   c[i,   i-1]           = -a[i+1]          (sub-diag, even i >= 2, < n)
  #   c[i,   i-2]           = 1                (second sub, odd i >= 3, < n)
  i = jnp.arange(n)[:, None]
  j = jnp.arange(n)[None, :]
  # Clip indices so out-of-range lookups are safe; masks below select valid
  # cells.
  super_val = -a[jnp.minimum(i + 2, n)]
  sub_val = -a[jnp.minimum(i + 1, n)]
  i_even = (i % 2 == 0)
  i_odd = (i % 2 == 1)
  one = jnp.array(1, dtype=a.dtype)
  zero = jnp.array(0, dtype=a.dtype)
  conditions = [
      (i == 0) & (j == 0),
      (i == 1) & (j == 0),
      (j == i + 1) & i_even,
      (j == i + 2) & i_even,
      (j == i - 1) & i_even & (i >= 2),
      (j == i - 2) & i_odd & (i >= 3),
  ]
  choices = [-a[1], one, super_val, one, sub_val, one]
  return jnp.select(conditions, choices, default=zero)

