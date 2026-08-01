
def _from_edtype_abstract_eval(x, *, dtype):
  assert (isinstance(x.dtype, dtypes.ExtendedDType) and
          not isinstance(dtype, dtypes.ExtendedDType))
  if not isinstance(x, ShapedArray):
    raise TypeError("can only convert from an extended dtype on an array type,"
                    f"but got {type(x)}")
  if convert_from := getattr(x.dtype._rules, 'convert_from', None):
    allow_conversion = convert_from(x.dtype, dtype)
  else:
    allow_conversion = x.dtype._rules.allow_conversion
  if not allow_conversion:
    raise ValueError(
        f"Cannot convert_element_type from {dtype_to_string(x.dtype)} "
        f"to {dtype_to_string(dtype)}")
  rep_aval = core.physical_element_aval(x.dtype)
  assert tuple(rep_aval.sharding.spec) == (None,) * rep_aval.ndim
  if rep_aval.dtype != dtype:
    raise ValueError(
        "can only convert from extended dtype to its representation dtype, "
        f"but tried to convert from {dtype_to_string(x.dtype)} to "
        f"{dtype_to_string(dtype)} which doesn't match the representation type "
        f"{dtype_to_string(rep_aval.dtype)}.")
  if isinstance(x, ShapedArray):
    return x.update(shape=(*x.shape, *rep_aval.shape), dtype=dtype)
  else:
    assert False  # unreachable, see isinstance check above

