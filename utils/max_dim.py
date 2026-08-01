
def max_dim(self: list[int], dim: int, keep_dim: bool):
    out = sum_mean_dim(self, [dim], keep_dim, None)
    return out, out


def max_dim(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    dtype = new_kwargs["input"].dtype
    dtype_min = _get_padding_value(dtype, "min")
    return _apply_reduction(func, "max", dtype_min, *args, **kwargs)


def max_dim(d1: DimSize, d2: DimSize) -> DimSize:
  """Like max(d1, d2) but for both constant and symbolic dimensions."""
  d1_is_constant = is_constant_dim(d1)
  if d1_is_constant and is_constant_dim(d2):
      return max(d1, d2)
  d1 = concrete_dim_or_error(d1, "argument `d1` of `core.max_dim`")
  d2 = concrete_dim_or_error(d2, "argument `d2` of `core.max_dim`")
  if d1_is_constant:
    return d2.rmax(d1)
  else:
    return d1.max(d2)

