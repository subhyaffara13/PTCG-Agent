import functools
from typing import Callable

def _searchsorted_impl(sorted_arr: ArrayLike, query: ArrayLike, *, dimension: int,
                       batch_dims: int, side: str, dtype: np.dtype, method: str):
  """Main implementation of searchsorted primitive."""
  sorted_arr = jnp.moveaxis(sorted_arr, dimension, -1)
  dtype = dtypes._maybe_canonicalize_explicit_dtype(dtype, "searchsorted")

  if method == "scan":
    impl: Callable[..., Array] = functools.partial(_searchsorted_scan_impl, unrolled=False)
  elif method == "scan_unrolled":
    impl = functools.partial(_searchsorted_scan_impl, unrolled=True)
  elif method == "compare_all":
    impl = _searchsorted_compare_all_impl
  elif method == "sort":
    impl = _searchsorted_sort_impl
  else:
    raise ValueError(f"Unsupported method: {method}")

  fun = functools.partial(impl, side=side, dtype=dtype)
  for _ in range(sorted_arr.ndim - batch_dims - 1):
    fun = api.vmap(fun, in_axes=(0, None))
  for _ in range(batch_dims):
    fun = api.vmap(fun, in_axes=0)
  return fun(sorted_arr, query)

