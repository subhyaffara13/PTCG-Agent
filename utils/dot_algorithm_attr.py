
def dot_algorithm_attr(precision: CanonicalPrecision, lhs_dtype: DTypeLike,
                       rhs_dtype: DTypeLike) -> hlo.DotAlgorithm | None:
  if not isinstance(precision, (DotAlgorithm, DotAlgorithmPreset)):
    return None
  return precision._convert_to_hlo_attr(lhs_dtype, rhs_dtype)

