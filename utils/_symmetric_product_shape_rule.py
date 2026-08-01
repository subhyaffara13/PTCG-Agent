
def _symmetric_product_shape_rule(a_shape, c_shape, **_):
  if a_shape[0] != c_shape[1] or c_shape[0] != c_shape[1]:
    raise ValueError(
        "symmetric_update expects a rectangular matrix of shape (m, n) and a "
        f"square matrix of shape (n, n). Got shapes {a_shape} and {c_shape}.")
  return c_shape

