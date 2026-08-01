
def _ndarray_constant_handler(val: np.ndarray | np.generic,
                              aval: core.AbstractValue | None) -> IrValues:
  """Constant handler for ndarray literals, handling zero-size strides.

  In most cases this function calls _numpy_array_constant(val) except it has
  special handling of arrays with any strides of size zero: for those, it
  generates appropriate calls to NumpyArrayConstant, Broadcast, and Transpose
  to avoid staging in large literals that might arise from np.zeros or np.ones
  or the output of lax.broadcast (which uses np.broadcast_to which in turn
  uses size-zero strides).

  Args:
    val: an ndarray.

  Returns:
    An XLA ComputationDataHandle / XlaOp representing the constant ndarray
    staged into the XLA Computation.
  """
  if val.dtype == dtypes.float0:
    return _numpy_array_constant(np.zeros(val.shape, dtype=np.bool_))
  elif 0 in val.strides and val.size > 0:
    zero_stride_axes, = np.where(np.equal(0, val.strides))
    other_axes, = np.where(np.not_equal(0, val.strides))
    collapsed_val = val[tuple(0 if ax in zero_stride_axes else slice(None)  # pyrefly: ignore[bad-index]
                              for ax in range(val.ndim))]
    out = hlo.broadcast_in_dim(
        ir.RankedTensorType.get(
            val.shape, dtype_to_ir_type(collapsed_val.dtype)),
        _numpy_array_constant(collapsed_val),
        dense_int_array(other_axes))  # pyrefly: ignore[bad-argument-type]
    return out
  else:
    return _numpy_array_constant(val)

