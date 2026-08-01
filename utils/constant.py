
def constant(image: Image.Image, value: int) -> Image.Image:
    """Fill a channel with a given gray level.

    :rtype: :py:class:`~PIL.Image.Image`
    """

    return Image.new("L", image.size, value)


def constant(
    result: Type, value: Union[int, float, Attribute, _array], *, loc=None, ip=None
) -> Value:
    return _get_op_result_or_op_results(ConstantOp(result, value, loc=loc, ip=ip))


def constant(value: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConstantOp(value=value, results=results, loc=loc, ip=ip).result


def constant(value: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConstantOp(value=value, results=results, loc=loc, ip=ip).result


def constant(result: _ods_ir.Type, value: _Union[str, _ods_ir.FlatSymbolRefAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConstantOp(result=result, value=value, loc=loc, ip=ip).result


def constant(value: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConstantOp(value=value, results=results, loc=loc, ip=ip).result


def constant(value: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConstantOp(value=value, results=results, loc=loc, ip=ip).result


def constant(value: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConstantOp(value=value, results=results, loc=loc, ip=ip).result


def constant(step_size) -> Schedule:
  def schedule(i):
    return step_size
  return schedule


def constant(value: ArrayLike,
             dtype: DTypeLikeInexact | None = None) -> Initializer:
  """Builds an initializer that returns arrays full of a constant ``value``.

  Args:
    value: the constant value with which to fill the initializer.
    dtype: optional; the initializer's default dtype.

  >>> import jax, jax.numpy as jnp
  >>> initializer = jax.nn.initializers.constant(-7)
  >>> initializer(jax.random.key(42), (2, 3), jnp.float32)
  Array([[-7., -7., -7.],
         [-7., -7., -7.]], dtype=float32)
  """
  def init(key: Array,
           shape: core.Shape,
           dtype: DTypeLikeInexact | None = dtype,
           out_sharding: OutShardingType = None) -> Array:
    dtype = dtypes.default_float_dtype() if dtype is None else dtype
    out_sharding = canonicalize_sharding(out_sharding, 'nn.initializers.constant')
    return jnp.full(shape, value, dtype=dtype, device=out_sharding)
  return init

