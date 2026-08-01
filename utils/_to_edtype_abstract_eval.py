
def _to_edtype_abstract_eval(x, *, edtype):
  assert (isinstance(edtype, dtypes.ExtendedDType) and
          not isinstance(x.dtype, dtypes.ExtendedDType))
  # For backward compatibility, if the edtype rules have a `convert_to` method,
  # use that rather than looking for an `allow_conversion: bool` attribute.
  if not isinstance(x, ShapedArray):
    raise TypeError("can only convert to an extended dtype on an array type,"
                    f"but got {type(x)}")
  if convert_to := getattr(edtype._rules, 'convert_to', None):
    allow_conversion = convert_to(x.dtype, edtype)
  else:
    allow_conversion = edtype._rules.allow_conversion
  if not allow_conversion:
    raise ValueError(
        f"Cannot convert_element_type from {dtype_to_string(x.dtype)} "
        f"to {dtype_to_string(edtype)}")
  rep_aval = core.physical_element_aval(edtype)
  assert tuple(rep_aval.sharding.spec) == (None,) * rep_aval.ndim
  if x.dtype != rep_aval.dtype:
    raise ValueError(
        "can only convert to extended dtype from its representation dtype, "
        f"but tried to convert from {dtype_to_string(x.dtype)} to "
        f"{dtype_to_string(edtype)} which doesn't match the representation type "
        f"{dtype_to_string(rep_aval.dtype)}.")
  if x.ndim < rep_aval.ndim:
    raise ValueError(
        "can only convert to extended dtype from an array of its "
        f"representation type, but the extended dtype {dtype_to_string(edtype)}"
        f" has a representation shape {rep_aval.shape} (rank {rep_aval.ndim}) "
        f"while the given representation array has shape {x.shape} (rank "
        f"{x.ndim} < {rep_aval.ndim}).")
  n = x.ndim - rep_aval.ndim
  shape_prefix, shape_suffix = x.shape[:n], x.shape[n:]
  if shape_suffix != rep_aval.shape:
    raise ValueError(
        "can only convert to extended dtype from an array of its "
        f"representation type, but the extended dtype {dtype_to_string(edtype)}"
        f" has a representation shape {rep_aval.shape} while the given "
        f"representation array has shape {x.shape}, so the shape suffix "
        f"does not match: given {shape_suffix} but required {rep_aval.shape}.")
  if isinstance(x, ShapedArray):
    spec_prefix, spec_suffix = x.sharding.spec[:n], x.sharding.spec[n:]
    if tuple(spec_suffix) != (None,) * len(spec_suffix):
      raise ValueError(
          "can only convert to extended dtype from an array with trailing "
          "axes that are not explicitly sharded, but tried to convert from "
          f"{x.str_short(short_dtypes=True)} to an extended dtype with element "
          f"shape {rep_aval.shape}")
    return x.update(shape=shape_prefix, dtype=edtype,
                    sharding=x.sharding.update(spec=spec_prefix))
  else:
    assert False  # unreachable, see isinstance check above

