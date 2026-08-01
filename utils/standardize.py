
def standardize(ctx, f, intervals, options):
    if options.get("ignore"):
        f = wrapsafe(f)
    finite = []
    infinite = []
    for k, points in enumerate(intervals):
        a, b = ctx._as_points(points)
        if b < a:
            return False, (lambda: ctx.zero)
        if a == ctx.ninf or b == ctx.inf:
            infinite.append((k, (a,b)))
        else:
            finite.append((k, (int(a), int(b))))
    if finite:
        f = fold_finite(ctx, f, finite)
        if not infinite:
            return False, lambda: f(*([0]*len(intervals)))
    if infinite:
        f = standardize_infinite(ctx, f, infinite)
        f = fold_infinite(ctx, f, infinite)
        args = [0] * len(intervals)
        d = infinite[0][0]
        def g(k):
            args[d] = k
            return f(*args)
        return True, g


def standardize(x: ArrayLike,
                axis: Axis = -1,
                mean: ArrayLike | None = None,
                variance: ArrayLike | None = None,
                epsilon: ArrayLike = 1e-5,
                where: ArrayLike | None = None,
                *,
                algorithm: str = "fast") -> Array:
  r"""Standardizes input to zero mean and unit variance.

  The standardization is given by:

  .. math::

     x_{std} = \frac{x - \langle x\rangle}{\sqrt{\langle(x - \langle x\rangle)^2\rangle + \epsilon}}

  where :math:`\langle x\rangle` indicates the mean of :math:`x`, and :math:`\epsilon` is
  a small correction factor introduced to avoid division by zero.

  Args:
    x: input array to be standardized.
    axis: integer, tuple of integers, or ``None`` (all axes), representing the
      axes along which to standardize. Defaults to the last axis (``-1``).
    mean: optionally specify the mean used for standardization. If not specified,
      then ``x.mean(axis, where=where)`` will be used.
    variance: optionally specify the variance used for standardization. If not
      specified, then ``x.var(axis, where=where)`` will be used.
    epsilon: correction factor added to variance to avoid division by zero; defaults
      to ``1E-5``.
    where: optional boolean mask specifying which elements to use when computing
      the mean and variance.
    algorithm: variance computation algorithm. ``"fast"`` uses ``mean(x^2) - mean(x)^2``
      which may be faster but can suffer from catastrophic cancellation and produce
      different results in eager vs JIT contexts. ``"stable"`` uses the two-pass
      formula ``mean((x - mean(x))^2)`` which is numerically stable. Default is
      ``"fast"`` for backward compatibility.

  Returns:
    An array of the same shape as ``x`` containing the standardized input.
  """
  numpy_util.check_arraylike("standardize", x)
  numpy_util.check_arraylike_or_none("standardize", mean, variance, where)
  if mean is None:
    mean = jnp.mean(x, axis, keepdims=True, where=where)
  if variance is None:
    if algorithm == "stable":
      variance = jnp.mean(
          jnp.square(jnp.subtract(x, mean)), axis, keepdims=True, where=where)
    elif algorithm == "fast":
      # This definition is traditionally seen as less accurate than the
      # two-pass mean((x - mean(x))**2) but may be faster and even, given
      # typical activation distributions and low-precision arithmetic, more
      # accurate when used in neural network normalization layers.
      variance = jnp.mean(
          jnp.square(x), axis, keepdims=True, where=where) - jnp.square(mean)
      # Because we're using a less accurate variance definition, it may
      # return negative values. This is problematic for the rsqrt, so we
      # clip to 0.
      variance = jnp.clip(variance, 0)
    else:
      raise ValueError(
          f"Unknown algorithm '{algorithm}'. Expected 'fast' or 'stable'.")
  return jnp.subtract(x, mean) * lax.rsqrt(variance + epsilon)

