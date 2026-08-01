
def searchsorted_via_expand(
    sorted_arr: ArrayLike,
    query: ArrayLike,
    /,
    *,
    side: str = "left",
    dimension: int = 0,
    batch_dims: int = 0,
    method: str = "scan",
    dtype: DTypeLike = "int32",
):
  """Compute searchsorted() without binding the hijax primitive."""
  sorted_arr, query = core.auto_insert_reshard(sorted_arr, query)
  out_dtype = dtypes._maybe_canonicalize_explicit_dtype(np.dtype(dtype), "searchsorted")
  prim = SearchSorted(
    core.typeof(sorted_arr),
    core.typeof(query),
    side=side,
    dimension=dimension,
    batch_dims=batch_dims,
    method=method,
    out_dtype=out_dtype,
  )
  return prim.expand(sorted_arr, query)

