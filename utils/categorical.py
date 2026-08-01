
def categorical(
  key: ArrayLike,
  logits: RealArray,
  axis: int = -1,
  shape: Shape | None = None,
  replace: bool = True,
  mode: str | None = None,
  *,
  out_sharding: NamedSharding | P | None = None
) -> Array:
  """Sample random values from categorical distributions.

  Sampling with replacement uses the Gumbel max trick. Sampling without replacement uses
  the Gumbel top-k trick. See [1] for reference.

  Args:
    key: a PRNG key used as the random key.
    logits: Unnormalized log probabilities of the categorical distribution(s) to sample from,
      so that `softmax(logits, axis)` gives the corresponding probabilities.
    axis: Axis along which logits belong to the same categorical distribution.
    shape: Optional, a tuple of nonnegative integers representing the result shape.
      Must be broadcast-compatible with ``np.delete(logits.shape, axis)``.
      The default (None) produces a result shape equal to ``np.delete(logits.shape, axis)``.
    replace: If True (default), perform sampling with replacement. If False, perform
      sampling without replacement.
    mode: optional, "high" or "low" for how many bits to use in the gumbel sampler.
      The default is determined by the ``use_high_dynamic_range_gumbel`` config,
      which defaults to "low". With mode="low", in float32 sampling will be biased
      for events with probability less than about 1E-7; with mode="high" this limit
      is pushed down to about 1E-14. mode="high" approximately doubles the cost of
      sampling.
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array with int dtype and shape given by ``shape`` if ``shape``
    is not None, or else ``np.delete(logits.shape, axis)``.

  References:
    .. [1] Wouter Kool, Herke van Hoof, Max Welling. "Stochastic Beams and Where to Find
      Them: The Gumbel-Top-k Trick for Sampling Sequences Without Replacement".
      Proceedings of the 36th International Conference on Machine Learning, PMLR
      97:3499-3508, 2019. https://proceedings.mlr.press/v97/kool19a.html.
  """
  key, _ = _check_prng_key("categorical", key)
  check_arraylike("categorical", logits)
  logits_arr = jnp.asarray(logits)
  batch_shape = tuple(np.delete(logits_arr.shape, axis))
  if shape is None:
    shape = batch_shape
  else:
    shape = core.canonicalize_shape(shape)
    _check_shape("categorical", shape, batch_shape)
  out_sharding = canonicalize_sharding(out_sharding, "categorical")
  return maybe_auto_axes(_categorical, out_sharding, shape=shape,
                         batch_shape=batch_shape, axis=axis,
                         replace=replace, mode=mode)(key, logits_arr)

