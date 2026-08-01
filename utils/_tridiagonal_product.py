
def _tridiagonal_product(dl, d, du, b):
  y = lax.reshape(d, d.shape + (1,)) * b
  y = y.at[..., 1:, :].add(dl[..., 1:, None] * b[..., :-1, :])
  y = y.at[..., :-1, :].add(du[..., :-1, None] * b[..., 1:, :])
  return y

