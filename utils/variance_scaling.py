
def variance_scaling(
  scale: RealNumeric,
  mode: Literal["fan_in"] | Literal["fan_out"] | Literal["fan_avg"] | Literal["fan_geo_avg"],
  distribution: (Literal["truncated_normal"] | Literal["normal"] |
                      Literal["uniform"]),
  in_axis: int | Sequence[int] = -2,
  out_axis: int | Sequence[int] = -1,
  batch_axis: int | Sequence[int] = (),
  dtype: DTypeLikeInexact | None = None
) -> Initializer:
  r"""
  Initializer that adapts its scale to the shape of the weights tensor.

  With ``distribution="truncated_normal"`` or ``distribution="normal"``, samples
  are drawn from a (truncated) normal distribution with a mean of zero
  and a standard deviation (after truncation, if applicable) of
  :math:`\sqrt{\frac{scale}{n}}`, where `n` is, for each ``mode``:

  * ``"fan_in"``: the number of inputs
  * ``"fan_out"``: the number of outputs
  * ``"fan_avg"``: the arithmetic average of the numbers of inputs and outputs
  * ``"fan_geo_avg"``: the geometric average of the numbers of inputs and outputs

  This initializer can be configured with ``in_axis``, ``out_axis``, and
  ``batch_axis`` to work with general convolutional or dense layers; axes that
  are not in any of those arguments are assumed to be the "receptive field"
  (convolution kernel spatial axes).

  With ``distribution="truncated_normal"``, the absolute values of the samples
  are truncated at 2 standard deviations before scaling.

  With ``distribution="uniform"``, samples are drawn from:

  * a uniform interval, if `dtype` is real, or
  * a uniform disk, if `dtype` is complex,

  with a mean of zero and a standard deviation of :math:`\sqrt{\frac{scale}{n}}`
  where `n` is defined above.

  Args:
    scale: scaling factor (positive float).
    mode: one of ``"fan_in"``, ``"fan_out"``, ``"fan_avg"``, and ``"fan_geo_avg"``.
    distribution: random distribution to use. One of ``"truncated_normal"``,
      ``"normal"`` and ``"uniform"``.
    in_axis: axis or sequence of axes of the input dimension in the weights
      array.
    out_axis: axis or sequence of axes of the output dimension in the weights
      array.
    batch_axis: axis or sequence of axes in the weight array that should be
      ignored.
    dtype: the dtype of the weights.
  """
  def init(key: Array,
           shape: core.Shape,
           dtype: DTypeLikeInexact | None = dtype,
           out_sharding: OutShardingType = None) -> Array:
    shape = core.canonicalize_shape(shape)
    dtype = dtypes.default_float_dtype() if dtype is None else dtype
    fan_in, fan_out = _compute_fans(shape, in_axis, out_axis, batch_axis)
    if mode == "fan_in": denominator = fan_in
    elif mode == "fan_out": denominator = fan_out
    elif mode == "fan_avg": denominator = (fan_in + fan_out) / 2
    elif mode == "fan_geo_avg": denominator = (fan_in * fan_out) ** 0.5
    else:
      raise ValueError(
        f"invalid mode for variance scaling initializer: {mode}")
    variance = jnp.array(scale / denominator, dtype=dtype)

    if distribution == "truncated_normal":
      if dtypes.issubdtype(dtype, np.floating):
        # constant is stddev of standard normal truncated to (-2, 2)
        stddev = jnp.sqrt(variance) / jnp.array(.87962566103423978, dtype)
        return random.truncated_normal(key, -2, 2, shape, dtype,
                                       out_sharding=out_sharding) * stddev
      else:
        # constant is stddev of complex standard normal truncated to 2
        stddev = jnp.sqrt(variance) / jnp.array(.95311164380491208, dtype)
        return _complex_truncated_normal(key, 2, shape, dtype) * stddev
    elif distribution == "normal":
      return random.normal(key, shape, dtype,
                           out_sharding=out_sharding) * jnp.sqrt(variance)
    elif distribution == "uniform":
      if dtypes.issubdtype(dtype, np.floating):
        return random.uniform(key, shape, dtype, -1,
                              out_sharding=out_sharding) * jnp.sqrt(3 * variance)
      else:
        return _complex_uniform(key, shape, dtype) * jnp.sqrt(variance)
    else:
      raise ValueError(f"invalid distribution for variance scaling initializer: {distribution}")

  return init

