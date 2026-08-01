
def broadcast_in_dim(a, shape, broadcast_dimensions):
    s = list(shape)
    for broadcast_dimension in broadcast_dimensions:
        s[broadcast_dimension] = -1

    v = a
    for idx, x in enumerate(s):
        if x != -1:
            v = unsqueeze(v, idx)

    return expand(v, shape)


def broadcast_in_dim(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.VectorType], broadcast_dimensions: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return BroadcastInDimOp(result=result, operand=operand, broadcast_dimensions=broadcast_dimensions, loc=loc, ip=ip).result


def broadcast_in_dim(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], broadcast_dimensions: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return BroadcastInDimOp(result=result, operand=operand, broadcast_dimensions=broadcast_dimensions, loc=loc, ip=ip).result


def broadcast_in_dim(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], broadcast_dimensions: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return BroadcastInDimOp(result=result, operand=operand, broadcast_dimensions=broadcast_dimensions, loc=loc, ip=ip).result


def broadcast_in_dim(operand, shape, broadcast_dimensions):
  in_reshape = np.ones(len(shape), dtype=np.int32)
  for i, bd in enumerate(broadcast_dimensions):
    in_reshape[bd] = operand.shape[i]
  return np.broadcast_to(np.reshape(operand, in_reshape), shape)


def broadcast_in_dim(ctx: LoweringRuleContext, op, aval_out: core.AbstractValue, *,
                     broadcast_dimensions) -> ir.Value:
  # broadcast_dimension[i] is the axis of the result where the axis i of
  # op is broadcast.
  # Lower a possibly-dynamic broadcast_in_dim
  if dtypes.issubdtype(aval_out.dtype, dtypes.extended):  # pyrefly: ignore[missing-attribute]
    elt_shape = core.physical_element_aval(aval_out.dtype).shape  # pyrefly: ignore[missing-attribute]
    trailing_dims = [aval_out.ndim + i for i in range(len(elt_shape))]  # pyrefly: ignore[missing-attribute]
    broadcast_dimensions = [*broadcast_dimensions, *trailing_dims]
    physical_aval_out = core.physical_aval(aval_out)
    return broadcast_in_dim(
        ctx, op, physical_aval_out, broadcast_dimensions=broadcast_dimensions)
  else:
    if not core.is_constant_shape(aval_out.shape):  # pyrefly: ignore[missing-attribute]
      shape = eval_dynamic_shape_as_tensor(ctx, aval_out.shape)  # pyrefly: ignore[missing-attribute]
      (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
      out = hlo.dynamic_broadcast_in_dim(
          result_type, op,
          shape,
          dense_int_array(broadcast_dimensions),
      )
    else:
      assert all(d != ir.ShapedType.get_dynamic_size()
                 for d in aval_out.shape), aval_out  # pyrefly: ignore[missing-attribute]
      (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
      out = hlo.broadcast_in_dim(
          result_type, op,
          dense_int_array(broadcast_dimensions))
    wrap_compute_type_in_place(ctx, out)
    return out


def broadcast_in_dim(operand: ArrayLike, shape: Shape,
                     broadcast_dimensions: Sequence[int], *, out_sharding=None
                     ) -> Array:
  """General broadcasting operation.

  This function lowers directly to the `stablehlo.broadcast_in_dim`_ operation.

  Args:
    operand: an array
    shape: the shape of the target array
    broadcast_dimensions: to which dimension in the target shape each dimension
      of the operand shape corresponds to. That is, dimension i of the operand
      becomes dimension broadcast_dimensions[i] of the result.

  Returns:
    An array containing the result.

  See also:
    - :func:`jax.lax.broadcast`: simpler interface to add new leading dimensions.
    - :func:`jax.numpy.broadcast_to`: NumPy-style API for general broadcasting.

  Examples:
    Here is an example of implementing simple NumPy-style broadcasting:

    >>> import jax.numpy as jnp
    >>> from jax import lax
    >>> import numpy as np

    >>> arr = jnp.arange(3).reshape(3, 1)
    >>> target_shape = (2, 3, 4)
    >>> result = lax.broadcast_in_dim(arr, target_shape, broadcast_dimensions=(1, 2))
    >>> result.shape
    (2, 3, 4)

    The above is equivalent to :func:`jax.numpy.broadcast_to`:

    >>> result_jnp = jnp.broadcast_to(result, target_shape)
    >>> np.testing.assert_array_equal(result, result_jnp)

    However, :func:`broadcast_in_dim` is more general, allowing implicit transposes
    as part of the single broadcasting operation:

    >>> result = lax.broadcast_in_dim(arr, target_shape, broadcast_dimensions=(1, 0))
    >>> result.shape
    (2, 3, 4)

    This more general operation has no direct equivlant in the NumPy-style broadcasting
    API, but can be replicated by appropriately adding and transposing input dimensions:

    >>> result_jnp = jnp.broadcast_to(jnp.expand_dims(arr, 0).transpose(), target_shape)
    >>> np.testing.assert_array_equal(result, result_jnp)

  .. _stablehlo.broadcast_in_dim: https://openxla.org/stablehlo/spec#broadcast_in_dim
  """
  out_sharding = canonicalize_sharding(out_sharding, 'broadcast_in_dim')
  if (np.ndim(operand) == len(shape) and not len(broadcast_dimensions) and
      isinstance(operand, Array) and out_sharding is None):
    return operand
  operand_aval = typeof(operand)
  if (operand_aval.shape == shape and
      list(broadcast_dimensions) == list(range(operand_aval.ndim)) and
      out_sharding is not None and operand_aval.sharding != out_sharding):
    return pjit.reshard(operand, out_sharding)
  return broadcast_in_dim_p.bind(
      operand, shape=tuple(shape),
      broadcast_dimensions=tuple(broadcast_dimensions), sharding=out_sharding)

