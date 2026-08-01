
def scalar_mul(xs, a):
  def mul(x):
    dtype = _dtype(x)
    result = np.multiply(x, np.array(a, dtype=dtype), dtype=dtype)
    return result.item() if is_python_scalar(x) else result
  return tree_map(mul, xs)

