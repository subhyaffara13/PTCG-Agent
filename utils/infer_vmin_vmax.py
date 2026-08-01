
def infer_vmin_vmax(
    array: np.ndarray,
    mask: np.ndarray,
    vmin: float | None,
    vmax: float | None,
    around_zero: bool,
    trim_outliers: bool,
) -> tuple[float, float]:
  """Infer reasonable lower and upper colormap bounds from an array."""
  inferring_both_bounds = vmax is None and vmin is None
  finite_mask = np.logical_and(np.isfinite(array), mask)
  if vmax is None:
    if around_zero:
      if vmin is not None:
        vmax = -vmin  # pylint: disable=invalid-unary-operand-type
      else:
        vmax = np.max(np.where(finite_mask, np.abs(array), 0))
    else:
      vmax = np.max(np.where(finite_mask, array, -np.inf))

  assert vmax is not None

  if vmin is None:
    if around_zero:
      vmin = -vmax  # pylint: disable=invalid-unary-operand-type
    else:
      vmin = np.min(np.where(finite_mask, array, np.inf))

  if inferring_both_bounds and trim_outliers:
    if around_zero:
      center = 0
    else:
      center = np.nanmean(np.where(finite_mask, array, np.nan))
      center = np.where(np.isfinite(center), center, 0.0)

    second_moment = np.nanmean(
        np.where(finite_mask, np.square(array - center), np.nan)
    )
    sigma = np.where(
        np.isfinite(second_moment), np.sqrt(second_moment), vmax - vmin
    )

    vmin_limit = center - 3 * sigma
    vmin = np.maximum(vmin, vmin_limit)
    vmax_limit = center + 3 * sigma
    vmax = np.minimum(vmax, vmax_limit)

  return vmin, vmax

