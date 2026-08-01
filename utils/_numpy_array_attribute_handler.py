
def _numpy_array_attribute_handler(val: np.ndarray | np.generic) -> ir.Attribute:
  if 0 in val.strides and val.size > 0:
    raise ValueError(
        "NumPy arrays with zero strides are not supported as MLIR attributes")
  if val.dtype == dtypes.float0:
    val = np.zeros(val.shape, dtype=np.bool_)
  if dtypes.is_weakly_typed_scalar(val) or np.isscalar(val):
    return _numpy_scalar_attribute(val)
  else:
    return _numpy_array_attribute(val)

