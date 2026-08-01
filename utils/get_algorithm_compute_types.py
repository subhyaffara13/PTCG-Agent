
def get_algorithm_compute_types(
    algorithm: DotAlgorithm | DotAlgorithmPreset,
    lhs_dtype: DTypeLike,
    rhs_dtype: DTypeLike,
    out_dtype: DTypeLike,
) -> tuple[DTypeLike, DTypeLike, DTypeLike]:
  if isinstance(algorithm, DotAlgorithm):
    return (
        algorithm.lhs_precision_type,
        algorithm.rhs_precision_type,
        algorithm.accumulation_type,
    )

  def maybe_convert_dtype(input_dtype: DTypeLike, target_dtypes: Sequence[DTypeLike] | None) -> DTypeLike:
    if target_dtypes is None:
      return input_dtype
    if np.dtype(input_dtype) in target_dtypes:
      return input_dtype
    return target_dtypes[0]

  lhs_dtype = maybe_convert_dtype(lhs_dtype, algorithm.supported_lhs_types)
  rhs_dtype = maybe_convert_dtype(rhs_dtype, algorithm.supported_rhs_types)
  out_type = maybe_convert_dtype(
      out_dtype, algorithm.supported_output_types(lhs_dtype, rhs_dtype)
  )
  return lhs_dtype, rhs_dtype, out_type

