
def broadcasted_iota(result: _ods_ir.Type, dimension: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return BroadcastedIotaOp(result=result, dimension=dimension, loc=loc, ip=ip).result


def broadcasted_iota(dtype: DTypeLike, shape: Shape, dimension: int,
                     *, out_sharding=None) -> Array:
  """Convenience wrapper around ``iota``."""
  dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "broadcasted_iota")
  shape = canonicalize_shape(shape)
  dimension = core.concrete_or_error(
      int, dimension, "dimension argument of lax.broadcasted_iota")
  out_sharding = canonicalize_sharding(out_sharding, 'broadcasted_iota')
  return iota_p.bind(dtype=dtype, shape=shape,
                     dimension=dimension, sharding=out_sharding)


def broadcasted_iota(
    dtype: jax.typing.DTypeLike,
    shape: Sequence[int],
    dimension: int,
    *,
    layout: SomeLayout | None = None,
) -> jax.Array:
  result = jax.lax.broadcasted_iota(dtype, shape, dimension)
  if layout is not None:
    result = gpu_core.layout_cast(result, layout)
  return result

