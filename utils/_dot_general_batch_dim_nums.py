
def _dot_general_batch_dim_nums(ndims, batch_dims, dimension_numbers):
  # There are three kinds of dimensions in a dot_general:
  # - contraction dimensions appear in lhs and rhs but not the result
  # - batch dimensions appear in lhs, rhs, and result
  # - tensor product dimensions appear in the result and one of lhs or rhs
  # The dimensions of the result are ordered as
  # - Batch dimensions
  #   - Q: In what order?  The order of appearance in lhs, rhs, or
  #     dimension_numbers?
  # - Tensor dimensions from the LHS
  # - Tensor dimensions from the RHS
  lhs_ndim, rhs_ndim = ndims
  # lbd and rbd are "batch" dimensions in the sense of dimensions being
  # vmapped, not to be confused with "batch" dimensions in the sense of
  # explicitly present dimensions that this dot_general is zipping together.
  lbd, rbd = batch_dims
  assert lbd is not None or rbd is not None
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = _from_maybe_ragged(dimension_numbers)

  is_ragged_dot = isinstance(dimension_numbers, RaggedDotDimensionNumbers)
  def bump_dims(dims, b):
    return tuple(np.add(dims, np.greater_equal(dims, b)))

  if type(lbd) is type(rbd) is int:
    # The vmapped dimensions become an additional batch dimension in the
    # batched dot_general, which we arbitrarily put first.
    lhs_batch = (lbd,) + bump_dims(lhs_batch, lbd)
    rhs_batch = (rbd,) + bump_dims(rhs_batch, rbd)
    lhs_contract = bump_dims(lhs_contract, lbd)
    rhs_contract = bump_dims(rhs_contract, rbd)
    result_batch_dim = 0
  elif (type(lbd) is int and rbd is None):
    # The left vmapped dimension becomes an additional tensor dimension in the
    # batched dot_general.
    lhs_tensor = [d for d in range(lhs_ndim)
                  if d not in lhs_batch and d not in lhs_contract]
    result_batch_dim = len(lhs_batch) + int(sum(np.less(lhs_tensor, lbd)))
    lhs_batch = bump_dims(lhs_batch, lbd)
    lhs_contract = bump_dims(lhs_contract, lbd)
  elif (type(rbd) is int and lbd is None):
    # The right vmapped dimension becomes an additional tensor dimension in the
    # batched dot_general.
    rhs_tensor = list(
        remaining(
            range(rhs_ndim),
            rhs_batch,
            rhs_contract,
            dimension_numbers.rhs_group_dimensions if is_ragged_dot else [],
        )
    )
    result_batch_dim = (lhs_ndim - len(lhs_contract) +
                        int(sum(np.less(rhs_tensor, rbd))))
    rhs_batch = bump_dims(rhs_batch, rbd)
    rhs_contract = bump_dims(rhs_contract, rbd)
  else:
    # We wouldn't be here if we didn't have at least one vmapped dimension.
    assert False

  new_dimension_numbers = ((lhs_contract, rhs_contract), (lhs_batch, rhs_batch))
  if is_ragged_dot:
    new_dimension_numbers = RaggedDotDimensionNumbers(
        dot_dimension_numbers=new_dimension_numbers,
        lhs_ragged_dimensions=bump_dims(
            dimension_numbers.lhs_ragged_dimensions, lbd
        ),
        rhs_group_dimensions=bump_dims(
            dimension_numbers.rhs_group_dimensions, rbd
        ),
    )
  return new_dimension_numbers, result_batch_dim

