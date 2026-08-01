
def dynamic_slice(operand: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], slice_sizes: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DynamicSliceOp(operand=operand, start_indices=start_indices, slice_sizes=slice_sizes, results=results, loc=loc, ip=ip).result


def dynamic_slice(operand: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], slice_sizes: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DynamicSliceOp(operand=operand, start_indices=start_indices, slice_sizes=slice_sizes, results=results, loc=loc, ip=ip).result


def dynamic_slice(operand, start_indices, slice_sizes):
  out = np.zeros(slice_sizes, dtype=operand.dtype)
  idx = tuple(_slice(start, start+size)
              for start, size in zip(start_indices, slice_sizes))
  section = operand[idx]
  out[tuple(_slice(None, stop) for stop in section.shape)] = section
  return out


def dynamic_slice(ctx: LoweringRuleContext, aval_out, x, *,
                  start_indices) -> ir.Value:
  x_aval = ctx.avals_in[0]
  if dtypes.issubdtype(aval_out.dtype, dtypes.extended):
    elt_shape = core.physical_element_aval(aval_out.dtype).shape
    index_avals = ctx.avals_in[1:]
    dtype = index_avals[0].dtype if index_avals else np.int32  # pyrefly: ignore[missing-attribute]
    trailing_zeros = [ir_constant(np.array(0, dtype))] * len(elt_shape)
    start_indices = (*start_indices, *trailing_zeros)
    aval_out = core.physical_aval(aval_out)
    x_aval = core.physical_aval(x_aval)

  slice_sizes = aval_out.shape
  if not core.is_constant_shape(slice_sizes):
    # lax.dynamic_slice clamps the start indices, but we are going to
    # lower to RealDynamicSliceOp, which is a version of SliceOp, and does
    # not have the clamping behavior. We clamp start ourselves.
    slice_sizes = eval_dynamic_shape_as_tensor(ctx, slice_sizes)
    clamped_start = hlo.clamp(
      shape_tensor(ctx.module_context, [0] * len(start_indices)),
      shape_tensor(ctx.module_context, start_indices),
      hlo.subtract(
        eval_dynamic_shape_as_tensor(ctx, x_aval.shape),  # pyrefly: ignore[missing-attribute]
        slice_sizes))
    (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
    return hlo.real_dynamic_slice(
        result_type, x,
        clamped_start,
        hlo.add(clamped_start, slice_sizes),
        shape_tensor(ctx.module_context, [1] * len(start_indices))
    )
  else:
    return hlo.dynamic_slice(x, start_indices, dense_int_array(slice_sizes))


def dynamic_slice(
    operand: Array | np.ndarray,
    start_indices: Array | np.ndarray | Sequence[ArrayLike],
    slice_sizes: Shape,
    *,
    allow_negative_indices: bool | Sequence[bool] = True
) -> Array:
  """Wraps XLA's `DynamicSlice
  <https://www.openxla.org/xla/operation_semantics#dynamicslice>`_
  operator.

  Args:
    operand: an array to slice.
    start_indices: a list of scalar indices, one per dimension. These values
      may be dynamic.
    slice_sizes: the size of the slice. Must be a sequence of non-negative
      integers with length equal to `ndim(operand)`. Inside a JIT compiled
      function, only static values are supported (all JAX arrays inside JIT
      must have statically known size).
    allow_negative_indices: a bool or sequence of bools, one per dimension; if
      a bool is passed, it applies to all dimensions. For each dimension,
      if true, negative indices are permitted and are are interpreted relative
      to the end of the array. If false, negative indices are treated as if they
      were out of bounds and the result is implementation defined, typically
      clamped to the first index.

  Returns:
    An array containing the slice.

  Examples:
    Here is a simple two-dimensional dynamic slice:

    >>> x = jnp.arange(12).reshape(3, 4)
    >>> x
    Array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]], dtype=int32)

    >>> dynamic_slice(x, (1, 1), (2, 3))
    Array([[ 5,  6,  7],
           [ 9, 10, 11]], dtype=int32)

    Note the potentially surprising behavior for the case where the requested slice
    overruns the bounds of the array; in this case the start index is adjusted to
    return a slice of the requested size:

    >>> dynamic_slice(x, (1, 1), (2, 4))
    Array([[ 4,  5,  6,  7],
           [ 8,  9, 10, 11]], dtype=int32)

  See Also:
    - :attr:`jax.numpy.ndarray.at`
    - :func:`jax.lax.slice`
    - :func:`jax.lax.dynamic_slice_in_dim`
    - :func:`jax.lax.dynamic_index_in_dim`
  """
  start_indices = _dynamic_slice_indices(
      operand, start_indices, allow_negative_indices)
  sizes = core.canonicalize_shape(slice_sizes)
  operand, *start_indices = core.auto_insert_reshard(operand, *start_indices)
  return dynamic_slice_p.bind(operand, *start_indices, slice_sizes=tuple(sizes))

