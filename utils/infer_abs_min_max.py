
def infer_abs_min_max(
    array: np.ndarray, mask: np.ndarray
) -> tuple[float, float]:
  """Infer smallest and largest absolute values in array."""
  finite_mask = np.logical_and(np.isfinite(array), mask)
  absmin = np.min(
      np.where(np.logical_and(finite_mask, array != 0), np.abs(array), np.inf)
  )
  absmin = np.where(np.isinf(absmin), 0.0, absmin)
  absmax = np.max(np.where(finite_mask, np.abs(array), -np.inf))
  absmax = np.where(np.isinf(absmax), 0.0, absmax)
  return absmin, absmax

