import math


def _unique_sorted_mask(ar: Array, axis: int, equal_nan: bool) -> tuple[Array, Array, Array]:
  aux = moveaxis(ar, axis, 0)
  if np.issubdtype(aux.dtype, np.complexfloating):
    # Work around issue in sorting of complex numbers with Nan only in the
    # imaginary component. This can be removed if sorting in this situation
    # is fixed to match numpy.
    aux = where(isnan(aux), lax._const(aux, np.nan), aux)
  size, *out_shape = aux.shape
  if math.prod(out_shape) == 0:
    size = 1
    perm = zeros(1, dtype=int)
  else:
    perm = lexsort(aux.reshape(size, math.prod(out_shape)).T[::-1])
  aux = aux[perm]
  if aux.size:
    if dtypes.issubdtype(aux.dtype, np.inexact) and equal_nan:
      # This is appropriate for both float and complex due to the documented behavior of np.unique:
      # See https://github.com/numpy/numpy/blob/v1.22.0/numpy/lib/arraysetops.py#L212-L220
      neq = lambda x, y: lax.ne(x, y) & ~(isnan(x) & isnan(y))
    else:
      neq = lax.ne
    mask = ones(size, dtype=bool).at[1:].set(any(neq(aux[1:], aux[:-1]), tuple(range(1, aux.ndim))))
  else:
    mask = zeros(size, dtype=bool)
  return aux, mask, perm

