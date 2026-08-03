import functools

def treemap_copy_args(f):
  @functools.wraps(f)
  def wrapper(*args, **kwargs):
    args, kwargs = jax.tree.map(lambda x: x, (args, kwargs))
    return f(*args, **kwargs)
  return wrapper

