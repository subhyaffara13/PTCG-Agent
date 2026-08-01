
def _cumsum_with_promotion(a: ArrayLike, axis: int | None = None,
           dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Utility function to compute cumsum with integer promotion."""
  return _cumulative_reduction("_cumsum_with_promotion", control_flow.cumsum,
                               a, axis, dtype, out, promote_integers=True)

