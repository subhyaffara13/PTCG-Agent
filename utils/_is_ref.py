
def _is_ref(x):
  from jax._src.state.types import AbstractRef
  try:
    return isinstance(typeof(x), AbstractRef)
  except:
    return False

