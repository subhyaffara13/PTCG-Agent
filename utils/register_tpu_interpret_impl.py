from typing import Callable

def register_tpu_interpret_impl(prim: jax_core.Primitive) -> Callable[[T], T]:
  """Registers an alternate primitive implementation for TPU Interpret Mode.

  User-defined primitives may register a custom Mosaic lowering.  To be able
  to run such a primitive in TPU Interpret Mode, a JAX implementation of the
  primitive must be registered using this function.
  """
  def decorator(impl: T) -> T:
    _interpret_impls[prim] = impl
    return impl

  return decorator

