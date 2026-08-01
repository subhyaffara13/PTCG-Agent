
def physical_aval(aval: ShapedArray) -> ShapedArray:
  ...


def physical_aval(aval: AbstractValue) -> AbstractValue:
  ...


def physical_aval(aval):
  if (isinstance(aval, ShapedArray) and
      isinstance(aval.dtype, dtypes.ExtendedDType)):
    elt_aval = physical_element_aval(aval.dtype)
    from jax._src.sharding_impls import physical_sharding  # pyrefly: ignore[missing-import]
    return ShapedArray((*aval.shape, *elt_aval.shape), elt_aval.dtype,
                       sharding=physical_sharding(aval, aval.sharding),
                       manual_axis_type=aval.mat,
                       memory_space=aval.memory_space)
  return aval

