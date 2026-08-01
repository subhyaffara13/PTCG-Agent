
def iota_2x32_shape(shape):
  """Reshaped ``uint64`` iota, as two parallel ``uint32`` arrays.

  Setting aside representation, this function essentially computes the
  equivalent of::

    jax.lax.iota(dtype=np.uint64, size=math.prod(shape)).reshape(shape)

  However:

  * It returns two parallel ``uint32`` arrays instead of one
    ``uint64`` array. This renders it invariant under either setting of
    the system-wide ``jax_enable_x64`` configuration flag.

  * It lowers in a way such that the compiler's automatic SPMD
    partitioner recognizes its partitionability.

  For example::

    >>> import numpy as np
    >>> from jax import lax
    >>> from jax._src.random import prng

    >>> prng.iota_2x32_shape((3, 4))
    [Array([[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]], dtype=uint32),
     Array([[ 0,  1,  2,  3],
            [ 4,  5,  6,  7],
            [ 8,  9, 10, 11]], dtype=uint32)]

    >>> def reshaped_iota(shape):
    ...   return lax.iota(size=math.prod(shape), dtype=np.uint32).reshape(shape)
    ...
    >>> reshaped_iota((3, 4))
    Array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]], dtype=uint32)

  Args:
    shape: the output shape

  Returns:
    A pair of ``uint32`` arrays ``(counts_hi, counts_lo)``, both of
    shape ``shape``, representing the higher-order and lower-order 32
    bits of the 64 bit unsigned iota.
  """
  if len(shape) == 0:
    return (jnp.zeros((), np.dtype('uint32')),) * 2
  return iota_2x32_shape_p.bind(shape=shape)

