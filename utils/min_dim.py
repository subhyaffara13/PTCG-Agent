
def min_dim(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    dtype = new_kwargs["input"].dtype
    dtype_max = _get_padding_value(dtype, "max")
    return _apply_reduction(func, "min", dtype_max, *args, **kwargs)


def min_dim(d1: DimSize, d2: DimSize) -> DimSize:
  """Like min(d1, d2) but for both constant and symbolic dimensions."""
  d1_is_constant = is_constant_dim(d1)
  if d1_is_constant and is_constant_dim(d2):
    return min(d1, d2)
  d1 = concrete_dim_or_error(d1, "argument `d1` of `core.min_dim`")
  d2 = concrete_dim_or_error(d2, "argument `d2` of `core.min_dim`")
  if d1_is_constant:
    return d2.rmin(d1)
  else:
    return d1.min(d2)

