
def _canonicalize_float_for_sort(x):
  # In the sort comparator, we are going to use a comparison operator where -0
  # would be before 0, and -NaN and NaN appear at the beginning and end of the
  # ordering. In this scheme, -0 would be before 0, and -NaN and NaN appear at
  # the beginning and end of the ordering. This causes issues for stable
  # sorts, so we avoid this by standardizing the representation of zeros
  # and NaNs in the output.
  result = select(eq(x, _zero(x)), _zeros(x), x)
  with config.debug_nans(False):
    result = select(_isnan(x), full_like(result, np.nan), result)
  return result

