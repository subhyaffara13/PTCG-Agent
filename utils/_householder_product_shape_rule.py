
def _householder_product_shape_rule(a_shape, taus_shape, **_):
  m, n = a_shape
  if m < n:
    raise ValueError(
        "The first argument to householder_product must have at least as many "
        f"rows as columns, got shape {a_shape}")
  k = taus_shape[0]
  if k > core.min_dim(m, n):
    raise ValueError(
        "The second argument to householder_product must not have more rows "
        "than the minimum of the first argument's rows and columns.")
  return a_shape

