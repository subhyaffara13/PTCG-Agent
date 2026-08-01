
def log_ndtr(a: TensorLikeType) -> TensorLikeType:
    # Note: M_SQRT1_2 is the value of 1 / sqrt(2)
    M_SQRT1_2 = 0.707106781186547524400844362104849039
    t = a * M_SQRT1_2
    return torch.where(
        a < 1.0,
        torch.log(torch.special.erfcx(-t) / 2) - t * t,
        torch.log1p(-torch.erfc(t) / 2),
    )


def log_ndtr(x: ArrayLike, series_order: int = 3) -> Array:
  r"""Log Normal distribution function.

  JAX implementation of :obj:`scipy.special.log_ndtr`.

  For details of the Normal distribution function see `ndtr`.

  This function calculates :math:`\log(\mathrm{ndtr}(x))` by either calling
  :math:`\log(\mathrm{ndtr}(x))` or using an asymptotic series. Specifically:

  - For `x > upper_segment`, use the approximation `-ndtr(-x)` based on
    :math:`\log(1-x) \approx -x, x \ll 1`.
  - For `lower_segment < x <= upper_segment`, use the existing `ndtr` technique
    and take a log.
  - For `x <= lower_segment`, we use the series approximation of `erf` to compute
    the log CDF directly.

  The `lower_segment` is set based on the precision of the input:

  .. math::
    \begin{align}
    \mathit{lower\_segment} =&
      \ \begin{cases}
        -20 &  x.\mathrm{dtype}=\mathit{float64} \\
        -10 &  x.\mathrm{dtype}=\mathit{float32} \\
        \end{cases} \\
    \mathit{upper\_segment} =&
      \ \begin{cases}
        8&  x.\mathrm{dtype}=\mathit{float64} \\
        5&  x.\mathrm{dtype}=\mathit{float32} \\
        \end{cases}
    \end{align}


  When `x < lower_segment`, the `ndtr` asymptotic series approximation is:

  .. math::
    \begin{align}
     \mathrm{ndtr}(x) =&\  \mathit{scale} * (1 + \mathit{sum}) + R_N \\
     \mathit{scale}   =&\  \frac{e^{-0.5 x^2}}{-x \sqrt{2 \pi}} \\
     \mathit{sum}     =&\  \sum_{n=1}^N {-1}^n (2n-1)!! / (x^2)^n \\
     R_N     =&\  O(e^{-0.5 x^2} (2N+1)!! / |x|^{2N+3})
    \end{align}

  where :math:`(2n-1)!! = (2n-1) (2n-3) (2n-5) ...  (3) (1)` is a
  `double-factorial
  <https://en.wikipedia.org/wiki/Double_factorial>`_ operator.


  Args:
    x: an array of type `float32`, `float64`.
    series_order: Positive Python integer. Maximum depth to
      evaluate the asymptotic expansion. This is the `N` above.

  Returns:
    an array with `dtype=x.dtype`.

  Raises:
    TypeError: if `x.dtype` is not handled.
    TypeError: if `series_order` is a not Python `integer.`
    ValueError:  if `series_order` is not in `[0, 30]`.
  """
  if not isinstance(series_order, int):
    raise TypeError("series_order must be a Python integer.")
  if series_order < 0:
    raise ValueError("series_order must be non-negative.")
  if series_order > 30:
    raise ValueError("series_order must be <= 30.")

  x_arr = jnp.asarray(x)
  dtype = lax.dtype(x_arr)

  if dtype == np.float64:
    lower_segment: np.ndarray = _LOGNDTR_FLOAT64_LOWER
    upper_segment: np.ndarray = _LOGNDTR_FLOAT64_UPPER
  elif dtype == np.float32:
    lower_segment = _LOGNDTR_FLOAT32_LOWER
    upper_segment = _LOGNDTR_FLOAT32_UPPER
  else:
    raise TypeError(f"x.dtype={np.dtype(dtype)} is not supported.")

  # The basic idea here was ported from:
  #   https://root.cern.ch/doc/v608/SpecFuncCephesInv_8cxx_source.html
  # We copy the main idea, with a few changes
  # * For x >> 1, and X ~ Normal(0, 1),
  #     Log[P[X < x]] = Log[1 - P[X < -x]] approx -P[X < -x],
  #     which extends the range of validity of this function.
  # * We use one fixed series_order for all of 'x', rather than adaptive.
  # * Our docstring properly reflects that this is an asymptotic series, not a
  #   Taylor series. We also provided a correct bound on the remainder.
  # * We need to use the max/min in the _log_ndtr_lower arg to avoid nan when
  #   x=0. This happens even though the branch is unchosen because when x=0
  #   the gradient of a select involves the calculation 1*dy+0*(-inf)=nan
  #   regardless of whether dy is finite. Note that the minimum is a NOP if
  #   the branch is chosen.
  x_arr_gt_upper_segment = lax.gt(x_arr, upper_segment)
  ndtr_arg = jnp.where(x_arr_gt_upper_segment, -x_arr,
                       lax.max(x_arr, lower_segment))
  # We combine both ndtr calls to minimize program size
  ndtr_res = _ndtr(ndtr_arg)
  return jnp.where(
      x_arr_gt_upper_segment,
      -ndtr_res,  # log(1-x) ~= -x, x << 1
      jnp.where(lax.gt(x_arr, lower_segment),
                       lax.log(ndtr_res),
                       _log_ndtr_lower(lax.min(x_arr, lower_segment),
                                       series_order)))

