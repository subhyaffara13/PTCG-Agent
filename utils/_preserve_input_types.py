
def _preserve_input_types(f):
  def wrapped(*args):
    dtype = _dtype(args[0])
    result = np.array(f(*args), dtype=dtype)
    if all(is_python_scalar(arg) for arg in args):
      result = result.item()
    return result
  return wrapped

