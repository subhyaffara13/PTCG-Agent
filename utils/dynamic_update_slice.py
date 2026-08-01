
def dynamic_update_slice(operand: _ods_ir.Value[_ods_ir.RankedTensorType], update: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DynamicUpdateSliceOp(operand=operand, update=update, start_indices=start_indices, results=results, loc=loc, ip=ip).result


def dynamic_update_slice(operand: _ods_ir.Value[_ods_ir.RankedTensorType], update: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DynamicUpdateSliceOp(operand=operand, update=update, start_indices=start_indices, results=results, loc=loc, ip=ip).result


def dynamic_update_slice(operand, update, start_indices):
  slices = tuple(_map(_slice, start_indices, np.add(start_indices, update.shape)))
  updated_operand = np.copy(operand)
  updated_operand[slices] = update
  return updated_operand


def dynamic_update_slice(ctx: LoweringRuleContext, aval_out, x, update, *,
                         start_indices) -> ir.Value:
  if dtypes.issubdtype(aval_out.dtype, dtypes.extended):
    elt_shape = core.physical_element_aval(aval_out.dtype).shape
    index_avals = ctx.avals_in[2:]
    dtype = index_avals[0].dtype if index_avals else np.int32  # pyrefly: ignore[missing-attribute]
    zeros = [ir_constant(np.array(0, dtype=dtype))] * len(elt_shape)
    start_indices = (*start_indices, *zeros)
    physical_aval_out = core.physical_aval(aval_out)
    return dynamic_update_slice(ctx, physical_aval_out, x, update,
                                start_indices=start_indices)
  else:
    # TODO(necula): handle dynamic shapes
    return hlo.dynamic_update_slice(x, update, start_indices)


def dynamic_update_slice(
    operand: Array | np.ndarray, update: ArrayLike,
    start_indices: Array | Sequence[ArrayLike],
    *,
    allow_negative_indices: bool | Sequence[bool] = True
) -> Array:
  """Wraps XLA's `DynamicUpdateSlice
  <https://www.openxla.org/xla/operation_semantics#dynamicupdateslice>`_
  operator.

  Args:
    operand: an array to slice.
    update: an array containing the new values to write onto `operand`.
    start_indices: a list of scalar indices, one per dimension.
    allow_negative_indices: a bool or sequence of bools, one per dimension; if
      a bool is passed, it applies to all dimensions. For each dimension,
      if true, negative indices are permitted and are are interpreted relative
      to the end of the array. If false, negative indices are treated as if they
      were out of bounds and the result is implementation defined, typically
      clamped to the first index.

  Returns:
    An array containing the slice.

  Examples:
    Here is an example of updating a one-dimensional slice update:

    >>> x = jnp.zeros(6)
    >>> y = jnp.ones(3)
    >>> dynamic_update_slice(x, y, (2,))
    Array([0., 0., 1., 1., 1., 0.], dtype=float32)

    If the update slice is too large to fit in the array, the start
    index will be adjusted to make it fit

    >>> dynamic_update_slice(x, y, (3,))
    Array([0., 0., 0., 1., 1., 1.], dtype=float32)
    >>> dynamic_update_slice(x, y, (5,))
    Array([0., 0., 0., 1., 1., 1.], dtype=float32)

    Here is an example of a two-dimensional slice update:

    >>> x = jnp.zeros((4, 4))
    >>> y = jnp.ones((2, 2))
    >>> dynamic_update_slice(x, y, (1, 2))
    Array([[0., 0., 0., 0.],
           [0., 0., 1., 1.],
           [0., 0., 1., 1.],
           [0., 0., 0., 0.]], dtype=float32)

  See Also:
    - :attr:`jax.numpy.ndarray.at`
    - :attr:`lax.dynamic_update_index_in_dim`
    - :attr:`lax.dynamic_update_slice_in_dim`
  """
  start_indices = _dynamic_slice_indices(
      operand, start_indices, allow_negative_indices)
  operand, update, *start_indices = core.auto_insert_reshard(
      operand, update, *start_indices)
  return dynamic_update_slice_p.bind(operand, update, *start_indices)

