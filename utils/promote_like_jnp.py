
def promote_like_jnp(fun, inexact=False):
  """Decorator that promotes the arguments of `fun` to `jnp.result_type(*args)`.

  jnp and np have different type promotion semantics; this decorator allows
  tests make an np reference implementation act more like a jnp
  implementation.
  """
  _promote = promote_dtypes_inexact if inexact else promote_dtypes
  def wrapper(*args, **kw):
    flat_args, tree = tree_flatten(args)
    args = tree_unflatten(tree, _promote(*flat_args))
    return fun(*args, **kw)
  return wrapper

