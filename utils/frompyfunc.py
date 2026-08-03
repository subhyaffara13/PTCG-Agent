from typing import Any, Callable

def frompyfunc(func: Callable[..., Any], /, nin: int, nout: int,
               *, identity: Any = None) -> ufunc:
  """Create a JAX ufunc from an arbitrary JAX-compatible scalar function.

  Args:
    func : a callable that takes `nin` scalar arguments and returns `nout` outputs.
    nin: integer specifying the number of scalar inputs
    nout: integer specifying the number of scalar outputs
    identity: (optional) a scalar specifying the identity of the operation, if any.

  Returns:
    wrapped : jax.numpy.ufunc wrapper of func.

  Examples:
    Here is an example of creating a ufunc similar to :obj:`jax.numpy.add`:

    >>> import operator
    >>> add = frompyfunc(operator.add, nin=2, nout=1, identity=0)

    Now all the standard :class:`jax.numpy.ufunc` methods are available:

    >>> x = jnp.arange(4)
    >>> add(x, 10)
    Array([10, 11, 12, 13], dtype=int32)
    >>> add.outer(x, x)
    Array([[0, 1, 2, 3],
           [1, 2, 3, 4],
           [2, 3, 4, 5],
           [3, 4, 5, 6]], dtype=int32)
    >>> add.reduce(x)
    Array(6, dtype=int32)
    >>> add.accumulate(x)
    Array([0, 1, 3, 6], dtype=int32)
    >>> add.at(x, 1, 10, inplace=False)
    Array([ 0, 11,  2,  3], dtype=int32)
  """
  return ufunc(func, nin, nout, identity=identity)

