
def ragged_dot_general(
    lhs: Array,
    rhs: Array,
    group_sizes: Array,
    ragged_dot_dimension_numbers: RaggedDotDimensionNumbers,
    precision: PrecisionLike = None,
    preferred_element_type: DTypeLike | None = None,
    group_offset: Array | None = None,
    out_sharding: NamedSharding | P | None = None,
) -> Array:
  """Ragged matrix multiplication.

  Ragged dot takes three arrays---``lhs``, ``rhs``, and ``group_sizes``---and
  a ``ragged_dot_dimension_numbers`` argument. Like `dot_general`, ``lhs`` and
  ``rhs`` are allowed arbitrary batch and contracting dimensions. Additionally,
  ``lhs`` is required to have one ragged dimension, and ``rhs`` may have at
  most one group dimension.

  Let `g` be the number of groups in the lhs ragged dimension. Ragged dot has
  three modes, depending on the kind of the lhs ragged dimension:

  1. ``[b...,m...,k...], [g,b...,k...,n...], [b...,x...,g] -> [b...,m...,n...]``.
     Here the ragged dimension is a non-contracting dimension (``m``) of ``lhs``,
     and ``x...`` are the lhs non-contracting dims outer to the ragged dim.
  2. ``[b...,m...,k...], [b...,k...,n...], [b...,x...,g] -> [g,b...,m...,n...]``.
     Here the ragged dimension is a contracting dimension (``k``) of ``lhs`` and
     ``rhs``, and `x...` are the lhs contracting dims outer to the ragged dim.
  3. ``[b...,m...,k...], [b...,k...,n...], [x...,g] -> [b...,m...,n...]``.
     Here the ragged dimension is a batch dimension (``b``) of ``lhs`` and
     ``rhs``, and ``x...`` are the lhs batch dims outer to the ragged dim.

  If ``group_sizes`` is passed-in with shape ``[g]``, it is broadcasted according
  to the rules above.

  Args:
    lhs: an array
    rhs: an array
    group_sizes: an array with integer element type
    ragged_dot_dimension_numbers: a ``RaggedDotDimensionNumbers`` object to
      specify the dot dimension numbers, lhs ragged dimension, and rhs group
      dimension.
    precision: Optional. Consistent with precision argument for
      :func:`jax.lax.dot`.
    preferred_element_type: Optional. Consistent with precision argument for
      :func:`jax.lax.dot`.
    group_offset: Optional. (1,) shaped array that indicates the group in
      group_sizes to start computing from. If not specified, defaults to [0].

  Results:
    An array whose shape is the same as that produced by `dot_general`, with an
    extra leading dimension of size `g` in the case where the lhs ragged
    dimension is a contracting dimension.
  """
  lhs, rhs, group_sizes = core.auto_insert_reshard(lhs, rhs, group_sizes)
  out_sharding = canonicalize_sharding(out_sharding, 'ragged_dot_general')
  return ragged_dot_general_p.bind(
      lhs,
      rhs,
      group_sizes,
      ragged_dot_dimension_numbers=ragged_dot_dimension_numbers,
      precision=canonicalize_precision(precision),
      preferred_element_type=preferred_element_type,
      group_offset=group_offset,
      out_sharding=out_sharding,
  )

