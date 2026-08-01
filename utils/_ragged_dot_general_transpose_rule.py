
def _ragged_dot_general_transpose_rule(
    ct,
    x,
    y,
    group_sizes,
    *,
    ragged_dot_dimension_numbers,
    precision,
    preferred_element_type: DTypeLike | None,
    group_offset: Array | None,
    out_sharding: NamedSharding | P | None = None,
):
  if group_offset is not None:
    raise NotImplementedError('Unimplemented group_offset support.')

  (x_contract, y_contract), (x_batch, y_batch) = ragged_dot_dimension_numbers.dot_dimension_numbers
  x_ndim = x.aval.ndim if ad.is_undefined_primal(x) else np.ndim(x)
  y_ndim = y.aval.ndim if ad.is_undefined_primal(y) else np.ndim(y)
  x_kept = remaining(range(x_ndim), x_contract, x_batch)
  y_group = ragged_dot_dimension_numbers.rhs_group_dimensions
  y_kept = remaining(range(y_ndim), y_contract, y_batch, y_group)
  mode, lhs_ragged_dim = _ragged_dot_mode_and_dim(
      x_ndim, ragged_dot_dimension_numbers
  )

  unimplemented = lambda fn_name, ragged_dot_mode: NotImplementedError(
      f'Unimplemented {fn_name} for ragged dot general in mode '
      f'{ragged_dot_mode.name}.'
  )

  def grad_x_dims():
    match mode:
      case RaggedDotMode.RAGGED_NONCONTRACTING:
        ans_batch, _, ans_y = ranges_like(x_batch, x_kept, y_kept)
        dims = RaggedDotDimensionNumbers(
            dot_dimension_numbers=((ans_y, y_kept), (ans_batch, y_batch)),
            lhs_ragged_dimensions=[
                len(x_batch) + x_kept.index(lhs_ragged_dim)
            ],
            rhs_group_dimensions=y_group,
        )
        x_contract_sorted_by_y = list(
            np.take(x_contract, np.argsort(y_contract))
        )
        unsorted_axes = list(x_batch) + x_kept + x_contract_sorted_by_y
      case RaggedDotMode.RAGGED_CONTRACTING | RaggedDotMode.RAGGED_BATCH | _:
        raise unimplemented('grad_x_dims', mode)
    return dims, unsorted_axes

  def grad_y_dims():
    match mode:
      case RaggedDotMode.RAGGED_NONCONTRACTING:
        ans_batch, ans_x, _ = ranges_like(x_batch, x_kept, y_kept)
        dims = RaggedDotDimensionNumbers(
            dot_dimension_numbers=((x_kept, ans_x), (x_batch, ans_batch)),
            lhs_ragged_dimensions=[lhs_ragged_dim],
            rhs_group_dimensions=[],
        )
        y_contract_sorted_by_x = list(
            np.take(y_contract, np.argsort(x_contract))
        )
        unsorted_axes = (
            list(y_group) + list(y_batch) + y_contract_sorted_by_x + y_kept
        )
      case RaggedDotMode.RAGGED_CONTRACTING | RaggedDotMode.RAGGED_BATCH | _:
        raise unimplemented('grad_y_dims', mode)
    return dims, unsorted_axes

  def _ragged_dot_grad(lhs, rhs, dims_fn, aval):
    dims, unsorted_axes = dims_fn()
    ragged_dot_general_out = ragged_dot_general(
          lhs, rhs, group_sizes, dims, precision=precision,
          preferred_element_type=preferred_element_type,
          group_offset=group_offset, out_sharding=aval.sharding)
    result = transpose(ragged_dot_general_out, tuple(np.argsort(unsorted_axes)))
    if result.dtype != aval.dtype:
      result = _convert_element_type(result, aval.dtype, aval.weak_type)
    return result

  x_bar = (
      None
      if ad.is_undefined_primal(y)
      else _ragged_dot_grad(ct, y, grad_x_dims, x.aval)
  )
  y_bar = (
      None
      if ad.is_undefined_primal(x)
      else _ragged_dot_grad(x, ct, grad_y_dims, y.aval)
  )
  return x_bar, y_bar, None

