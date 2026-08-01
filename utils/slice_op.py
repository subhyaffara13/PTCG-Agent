
def slice_op(ctx: LoweringRuleContext, x, aval_out, *,
             start_indices, limit_indices, strides) -> ir.Value:
  if dtypes.issubdtype(aval_out.dtype, dtypes.extended):
    elt_shape = core.physical_element_aval(aval_out.dtype).shape
    trailing_zeros = [0] * len(elt_shape)
    trailing_ones  = [1] * len(elt_shape)
    start_indices = (*start_indices, *trailing_zeros)
    limit_indices = (*limit_indices, *elt_shape)
    strides = (*strides, *trailing_ones)
    physical_aval_out = core.physical_aval(aval_out)
    return slice_op(ctx, x, physical_aval_out, start_indices=start_indices,
                    limit_indices=limit_indices, strides=strides)
  else:
    if any(not core.is_constant_shape(s) for s in (start_indices, limit_indices, strides)):
      start_indices = eval_dynamic_shape_as_tensor(ctx, start_indices)
      limit_indices = eval_dynamic_shape_as_tensor(ctx, limit_indices)
      strides = eval_dynamic_shape_as_tensor(ctx, strides)
      (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
      return hlo.real_dynamic_slice(
        result_type,
        x, start_indices, limit_indices, strides)
    else:
      return hlo.slice(x,
                       dense_int_array(start_indices),
                       dense_int_array(limit_indices),
                       dense_int_array(strides))

