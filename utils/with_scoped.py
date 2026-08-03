import functools
from typing import Any

def with_scoped(
    *types: Any,
    collective_axes: Hashable | tuple[Hashable, ...] = (),
    **kw_types: Any,
):
  """Returns a function decorator that runs a function with provided allocations.

  Example::

    @pl.with_scoped(pltpu.VMEM((8, 128), jnp.float32),
                    sem_ref=pltpu.SemaphoreType.DMA)
    def f(vmem_ref, sem_ref):
      ...

    f()

  The arguments to `f` will be forwarded to the decorated function as the
  initial arguments.

  Example::

    @pl.with_scoped(pltpu.VMEM((8, 128), jnp.float32),
                    sem_ref=pltpu.SemaphoreType.DMA)
    def f(outer_ref, vmem_ref, sem_ref):
      ...

    outer_ref = ...
    f(outer_ref)

  """
  def decorator(f):
    def inner(*args):
      return pl_primitives.run_scoped(
          functools.partial(f, *args),
          *types,
          collective_axes=collective_axes,
          **kw_types,
      )
    return inner
  return decorator

