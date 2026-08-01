
def _handle_dot_precision(ctx, lhs, rhs, precision, platform):
  def _is_fp8_mixed_precision_matmul(_lhs_dtypes, _rhs_dtypes):
    fp8_dtypes = (dtypes.float8_e4m3fn, dtypes.float8_e5m2,
                  dtypes.float8_e5m2fnuz, dtypes.float8_e4m3fnuz,
                  dtypes.float8_e3m4, dtypes.float8_e4m3,
                  dtypes.float8_e8m0fnu)
    return _lhs_dtypes in fp8_dtypes and _rhs_dtypes in fp8_dtypes

  # The *_ lets us reuse this for ragged_dot_general, which has group_sizes.
  lhs_aval, rhs_aval, *_ = ctx.avals_in
  lhs_dtype, rhs_dtype = lhs_aval.dtype, rhs_aval.dtype
  aval_out, = ctx.avals_out
  accumulation_aval = aval_out
  algorithm_kwarg = {}
  if isinstance(precision, (DotAlgorithm, DotAlgorithmPreset)):
    # The CPU backend silently ignores the algorithm spec, so we check here to
    # make sure that the selected algorithm is supported. We could be a little
    # bit more liberal here (any algorithm where the input and output types
    # match and all the other parameters have default values should work), but
    # it's probably sufficient to just check the presets here.
    if platform == "cpu" and precision not in {
        DotAlgorithmPreset.DEFAULT, DotAlgorithmPreset.F16_F16_F16,
        DotAlgorithmPreset.F32_F32_F32, DotAlgorithmPreset.F64_F64_F64,
        DotAlgorithmPreset.BF16_BF16_F32, DotAlgorithmPreset.BF16_BF16_F32_X3,
        DotAlgorithmPreset.BF16_BF16_F32_X6,
    }:
      raise ValueError(
          f"The precision '{precision}' is not supported by dot_general on CPU")

    # If an explicit algorithm was specified, we always cast the input types to
    # the correct types.
    def maybe_convert_dtype(operand, operand_aval, target_dtype):
      if target_dtype is None or operand_aval.dtype == target_dtype:
        return operand
      aval = core.ShapedArray(operand_aval.shape, target_dtype)
      return mlir.convert_hlo(ctx, operand, operand_aval, aval)

    lhs_dtype, rhs_dtype, accumulation_dtype = get_algorithm_compute_types(
        precision, lhs_dtype, rhs_dtype, aval_out.dtype)
    lhs = maybe_convert_dtype(lhs, lhs_aval, lhs_dtype)
    rhs = maybe_convert_dtype(rhs, rhs_aval, rhs_dtype)
    if accumulation_dtype is not None:
      accumulation_aval = core.ShapedArray(aval_out.shape, accumulation_dtype)

    if precision != DotAlgorithmPreset.DEFAULT:
      algorithm_kwarg = {
          "algorithm": dot_algorithm_attr(precision, lhs_dtype, rhs_dtype)
      }
  else:
    # TODO(b/...): JAX's dot_general primitive accepts the same input dtype
    # combinations that are accepted in XLA's shape_inference.cc (the canonical
    # reference for the HLO type system), but actually different XLA platforms
    # fail on codegen for different accepted cases. To handle those cases, we
    # insert ConvertOps on the input, in a platform-dependent way.
    if lhs_dtype != rhs_dtype:
      if platform == "tpu":
        handled = lambda dt: (dtypes.issubdtype(dt, np.floating) or
                              dtypes.issubdtype(dt, np.integer))
        if not (handled(lhs_dtype) and handled(rhs_dtype)):
          lhs = mlir.convert_hlo(ctx, lhs, lhs_aval,
                                 core.ShapedArray(lhs_aval.shape, aval_out.dtype))
          rhs = mlir.convert_hlo(ctx, rhs, rhs_aval,
                                 core.ShapedArray(rhs_aval.shape, aval_out.dtype))
      else:  # cpu and gpu
        # Do not convert mixed fp8 types to output type.
        if not _is_fp8_mixed_precision_matmul(lhs_dtype, rhs_dtype):
          lhs = mlir.convert_hlo(ctx, lhs, lhs_aval,
                                 core.ShapedArray(lhs_aval.shape, aval_out.dtype))
          rhs = mlir.convert_hlo(ctx, rhs, rhs_aval,
                                 core.ShapedArray(rhs_aval.shape, aval_out.dtype))
  return lhs, rhs, accumulation_aval, algorithm_kwarg

