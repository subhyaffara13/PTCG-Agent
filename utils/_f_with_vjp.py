from typing import Callable

def _f_with_vjp(f: Callable):
  @util.wraps(f)
  def wrapped(*args):
    primals, f_vjp = api.vjp(f, *args)
    return f_vjp(tree_map(jnp.bfloat16, primals))

  return wrapped

