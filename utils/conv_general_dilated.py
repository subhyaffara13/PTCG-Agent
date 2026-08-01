
def conv_general_dilated(lhs, rhs, window_strides, padding, lhs_dilation,
                         rhs_dilation, dimension_numbers):
  lhs_perm, rhs_perm, out_perm = _conv_general_permutations(dimension_numbers)
  if isinstance(padding, str):
    padding = padtype_to_pads(np.take(lhs.shape, lhs_perm)[2:],
                              np.take(rhs.shape, rhs_perm)[2:],
                              window_strides, padding)
  trans_lhs = transpose(lhs, lhs_perm)
  trans_rhs = transpose(rhs, rhs_perm)
  out = conv_with_general_padding(trans_lhs, trans_rhs, window_strides, padding,
                                  lhs_dilation, rhs_dilation)
  return transpose(out, np.argsort(out_perm))


def conv_general_dilated(
  lhs: Array, rhs: Array, window_strides: Sequence[int],
  padding: str | Sequence[tuple[int, int]],
  lhs_dilation: Sequence[int] | None = None,
  rhs_dilation: Sequence[int] | None = None,
  dimension_numbers: ConvGeneralDilatedDimensionNumbers  = None,
  feature_group_count: int = 1, batch_group_count: int = 1,
  precision: lax.PrecisionLike = None,
  preferred_element_type: DTypeLike | None = None,
  out_sharding: NamedSharding | P | None = None) -> Array:
  """General n-dimensional convolution operator, with optional dilation.

  Wraps XLA's `Conv
  <https://www.openxla.org/xla/operation_semantics#conv_convolution>`_
  operator.

  Args:
    lhs: a rank `n+2` dimensional input array.
    rhs: a rank `n+2` dimensional array of kernel weights.
    window_strides: a sequence of `n` integers, representing the inter-window
      strides.
    padding: either the strings `'SAME'`, `'SAME_LOWER'`, or `'VALID'`, or a
      sequence of `n` `(low, high)` integer pairs that give the padding to apply
      before and after each spatial dimension. `'SAME'` and `'SAME_LOWER'` add
      padding to produce same output size as the input. The padding is split
      between the two sides equally or almost equally. In case the padding is an
      odd number, the extra padding is added at the end for `'SAME'` and at the
      beginning for `'SAME_LOWER'`.
    lhs_dilation: `None`, or a sequence of `n` integers, giving the dilation
      factor to apply in each spatial dimension of `lhs`. LHS dilation is also
      known as transposed convolution.
    rhs_dilation: `None`, or a sequence of `n` integers, giving the dilation
      factor to apply in each spatial dimension of `rhs`. RHS dilation is also
      known as atrous convolution.
    dimension_numbers: either `None`, a ``ConvDimensionNumbers`` object, or a
      3-tuple ``(lhs_spec, rhs_spec, out_spec)``, where each element is a string
      of length `n+2`.
    feature_group_count: integer, default 1. See XLA HLO docs.
    batch_group_count: integer, default 1. See XLA HLO docs.
    precision: Optional. Either ``None``, which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value
      (``Precision.DEFAULT``, ``Precision.HIGH`` or ``Precision.HIGHEST``), a
      string (e.g. 'highest' or 'fastest', see the
      ``jax.default_matmul_precision`` context manager), or a tuple of two
      :class:`~jax.lax.Precision` enums or strings indicating precision of
      ``lhs`` and ``rhs``.
    preferred_element_type: Optional. Either ``None``, which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    An array containing the convolution result.

  In the string case of ``dimension_numbers``, each character identifies by
  position:

  - the batch dimensions in ``lhs``, ``rhs``, and the output with the character
    'N',
  - the feature dimensions in `lhs` and the output with the character 'C',
  - the input and output feature dimensions in rhs with the characters 'I'
    and 'O' respectively, and
  - spatial dimension correspondences between lhs, rhs, and the output using
    any distinct characters. The examples below use 'W' and 'H'.

  For example, to indicate dimension numbers consistent with the ``conv``
  function with two spatial dimensions, one could use ``('NCHW', 'OIHW',
  'NCHW')``. As another example, to indicate dimension numbers consistent with
  the TensorFlow Conv2D operation, one could use ``('NHWC', 'HWIO', 'NHWC')``.
  When using the latter form of convolution dimension specification, window
  strides are associated with spatial dimension character labels according to
  the order in which the labels appear in the ``rhs_spec`` string, so that
  ``window_strides[0]`` is matched with the dimension corresponding to the first
  character appearing in rhs_spec that is not ``'I'`` or ``'O'``.

  If ``dimension_numbers`` is ``None``, the default is ``('NCHW', 'OIHW',
  'NCHW')`` (for a 2D convolution).
  """
  dnums = conv_dimension_numbers(lhs.shape, rhs.shape, dimension_numbers)
  out_sharding = canonicalize_sharding(out_sharding, 'dot_general')
  if lhs_dilation is None:
    lhs_dilation = (1,) * (lhs.ndim - 2)
  elif isinstance(padding, str) and not len(lhs_dilation) == lhs_dilation.count(1):
    raise ValueError(
        "String padding is not implemented for transposed convolution "
        "using this op. Please either exactly specify the required padding or "
        "use conv_transpose.")
  if rhs_dilation is None:
    rhs_dilation = (1,) * (rhs.ndim - 2)
  if isinstance(padding, str):
    lhs_perm, rhs_perm, _ = dnums
    rhs_shape = np.take(rhs.shape, rhs_perm)[2:]
    effective_rhs_shape = [core.dilate_dim(k, r) for k, r in zip(rhs_shape, rhs_dilation)]
    padding = lax.padtype_to_pads(
        np.take(lhs.shape, lhs_perm)[2:], effective_rhs_shape,
        window_strides, padding)
  else:
    try:
      padding = tuple((operator.index(lo), operator.index(hi))
                      for lo, hi in padding)
    except (ValueError, TypeError) as e:
      raise ValueError(
        "padding argument to conv_general_dilated should be a string or a "
        f"sequence of (low, high) pairs, got {padding}") from e

  preferred_element_type = (
      None if preferred_element_type is None
      else dtypes.check_and_canonicalize_user_dtype(
          preferred_element_type, "conv_general_dilated"
      )
  )
  lhs, rhs = core.auto_insert_reshard(lhs, rhs)
  return conv_general_dilated_p.bind(
      lhs, rhs, window_strides=tuple(window_strides), padding=tuple(padding),
      lhs_dilation=tuple(lhs_dilation), rhs_dilation=tuple(rhs_dilation),
      dimension_numbers=dnums,
      feature_group_count=feature_group_count,
      batch_group_count=batch_group_count,
      precision=lax.canonicalize_precision(precision),
      preferred_element_type=preferred_element_type,
      out_sharding=out_sharding)

