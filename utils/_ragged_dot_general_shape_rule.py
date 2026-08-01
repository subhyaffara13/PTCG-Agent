
def _ragged_dot_general_shape_rule(
    lhs,
    rhs,
    group_sizes,
    *,
    ragged_dot_dimension_numbers,
    precision,
    preferred_element_type: DTypeLike | None,
    group_offset,
    out_sharding,
):
  def _check_in_range(dim, rank, dim_name, arg_name):
    if dim < 0 or dim >= rank:
      raise TypeError(
          f'ragged_dot_general requires {dim_name} numbers to be nonnegative '
          f'and less than the number of axes of the {arg_name} value, '
          f'got {dim} for {arg_name} of rank {rank}.'
      )

  # Validate the lhs ragged dimension, and find out which mode we're in.
  if len(ragged_dot_dimension_numbers.lhs_ragged_dimensions) != 1:
    raise TypeError(
        'ragged_dot_general expects exactly one lhs ragged dimension.'
    )
  lhs_ragged_dim = ragged_dot_dimension_numbers.lhs_ragged_dimensions[0]
  _check_in_range(lhs_ragged_dim, lhs.ndim, 'lhs ragged dimension', 'lhs')
  mode = _ragged_dot_mode(lhs.ndim, ragged_dot_dimension_numbers)

  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = (
      ragged_dot_dimension_numbers.dot_dimension_numbers
  )

  # Validate the shape of group_sizes, if it is something other than [g].
  if group_sizes.ndim == 0:
    raise TypeError('expected rank of group_sizes to be >=1.')
  if group_sizes.ndim != 1:
    # Construct the expected shape [b...,x...,g] of group_sizes.
    prefix_dims = _ragged_dot_prefix_dims(
        mode, lhs.ndim, lhs_ragged_dim, lhs_batch, lhs_contracting
    )
    expected_gs_shape = tuple(lhs.shape[i] for i in prefix_dims)
    expected_gs_shape += (group_sizes.shape[-1],)
    # TODO(pravnar): Permit other broadcastable shapes.
    if not core.definitely_equal_shape(group_sizes.shape, expected_gs_shape):
      raise TypeError(
          'expected group_sizes to have shape '
          f'{expected_gs_shape}, got {group_sizes.shape}.'
      )
  num_groups = group_sizes.shape[-1]
  if (mode in (RaggedDotMode.RAGGED_CONTRACTING,
               RaggedDotMode.RAGGED_NONCONTRACTING)
      and core.is_symbolic_dim(num_groups)):
    raise TypeError(
        'ragged_dot_general requires the group count (last dimension of '
        'group_sizes) to be static in Mode 1 (non-contracting) and Mode 2 '
        '(contracting).'
    )

  # Validate properties of the rhs group dimension(s).
  rhs_group_dims = ragged_dot_dimension_numbers.rhs_group_dimensions
  match mode:
    case RaggedDotMode.RAGGED_CONTRACTING | RaggedDotMode.RAGGED_BATCH:
      if len(rhs_group_dims) != 0:
        raise TypeError(
            'ragged_dot_general requires zero group dimensions in the rhs '
            'when lhs ragged dimension is contracting or batch.'
        )
    case RaggedDotMode.RAGGED_NONCONTRACTING:
      if len(rhs_group_dims) != 1:
        raise TypeError(
            'ragged_dot_general requires exactly one rhs group dimension '
            'when lhs ragged dimension is noncontracting.'
        )
      rhs_group_dim = rhs_group_dims[0]
      _check_in_range(rhs_group_dim, rhs.ndim, 'rhs group dimension', 'rhs')
      if rhs_group_dim in rhs_batch or rhs_group_dim in rhs_contracting:
        raise TypeError(
            'ragged_dot_general requires rhs group dimension numbers to be '
            'distinct from contracting and batch dimensions.'
        )
      if rhs.shape[rhs_group_dim] != num_groups:
        raise TypeError(
            'expected rhs group dimension size to be '
            f'{num_groups}, got {rhs.shape[rhs_group_dim]}.'
        )

  out_shape = _dot_general_shape_rule(
      lhs,
      rhs,
      dimension_numbers=ragged_dot_dimension_numbers,
      precision=precision,
      preferred_element_type=preferred_element_type,
      out_sharding=None,
  )
  if mode == RaggedDotMode.RAGGED_CONTRACTING:
    out_shape = (num_groups,) + out_shape
  return out_shape

