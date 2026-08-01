
def dot_general(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], dot_dimension_numbers: _Union[_Any, _ods_ir.Attribute], *, precision_config: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, algorithm: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DotGeneralOp(result=result, lhs=lhs, rhs=rhs, dot_dimension_numbers=dot_dimension_numbers, precision_config=precision_config, algorithm=algorithm, loc=loc, ip=ip).result


def dot_general(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], dot_dimension_numbers: _Union[_Any, _ods_ir.Attribute], *, precision_config: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, algorithm: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DotGeneralOp(result=result, lhs=lhs, rhs=rhs, dot_dimension_numbers=dot_dimension_numbers, precision_config=precision_config, algorithm=algorithm, loc=loc, ip=ip).result


def dot_general(lhs, rhs, dimension_numbers):
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers
  new_id = itertools.count()
  lhs_axis_ids: list[int | None] = [next(new_id) for _ in lhs.shape]
  rhs_axis_ids: list[int | None] = [next(new_id) for _ in rhs.shape]
  lhs_out_axis_ids = lhs_axis_ids[:]
  rhs_out_axis_ids = rhs_axis_ids[:]

  for lhs_axis, rhs_axis in zip(lhs_contracting, rhs_contracting):
    shared_id = next(new_id)
    lhs_axis_ids[lhs_axis] = shared_id
    rhs_axis_ids[rhs_axis] = shared_id
    lhs_out_axis_ids[lhs_axis] = None
    rhs_out_axis_ids[rhs_axis] = None

  batch_ids = []
  for lhs_axis, rhs_axis in zip(lhs_batch, rhs_batch):
    shared_id = next(new_id)
    lhs_axis_ids[lhs_axis] = shared_id
    rhs_axis_ids[rhs_axis] = shared_id
    lhs_out_axis_ids[lhs_axis] = None
    rhs_out_axis_ids[rhs_axis] = None
    batch_ids.append(shared_id)

  not_none = lambda x: x is not None
  out_axis_ids = filter(not_none,
                        batch_ids + lhs_out_axis_ids + rhs_out_axis_ids)
  assert lhs.dtype == rhs.dtype
  dtype = np.float32 if lhs.dtype == dtypes.bfloat16 else None
  out = np.einsum(  # pyrefly: ignore[no-matching-overload]
      lhs, lhs_axis_ids, rhs, rhs_axis_ids, out_axis_ids, dtype=dtype
  )
  return out.astype(dtypes.bfloat16) if lhs.dtype == dtypes.bfloat16 else out


def dot_general(lhs: ArrayLike, rhs: ArrayLike,
                dimension_numbers: DotDimensionNumbers,
                precision: PrecisionLike = None,
                preferred_element_type: DTypeLike | None = None,
                *,
                out_sharding=None) -> Array:
  """Alias of :func:`jax.lax.dot`.

  Prefer use of :func:`jax.lax.dot` directly, but note that it requires
  all arguments after ``lhs`` and ``rhs`` to be specified by keyword
  rather than position.
  """
  return dot(lhs, rhs, dimension_numbers=dimension_numbers, precision=precision,
             preferred_element_type=preferred_element_type, out_sharding=out_sharding)

