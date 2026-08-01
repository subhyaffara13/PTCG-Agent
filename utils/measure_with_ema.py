
def measure_with_ema(
    measure: Callable[[base.Updates], base.ArrayTree],
    decay: jax.typing.ArrayLike,  # float
    debias: bool = True,
    accumulator_dtype: Any | None = None
) -> base.GradientTransformationExtraArgs:
  """Take a measurement and record it with exponential moving average.

  Args:
    measure: User callable taking as inputs updates and returning desired
      measurement.
    decay: Decay rate for the exponential moving average.
    debias: Whether to debias the exponential moving average.
    accumulator_dtype: Optional dtype for the exponential moving average
      accumulator.

  Returns:
    A gradient transformation that captures measurements defined by the user,
    and records them with exponential moving average.

  .. seealso::
    :func:`optax.monitor`

  .. versionadded: 0.2.7
  """
  base_ema = _accumulation.ema(decay, debias, accumulator_dtype)

  def init_for_measurement(params):
    # ema needs to be initialized with a variable of the shape it will be
    # accumulated in. In this case, it is the shape of the measurement that can
    # be inferred from applying the measure to params.
    return base_ema.init(measure(params))

  measurement_ema = base_ema._replace(init=init_for_measurement)
  return _combining.chain(
      base.stateless(lambda updates, _: measure(updates)),
      measurement_ema
  )

