
def _linalg_ffi_lowering(target_name, avals_in=None, avals_out=None,
                         operand_output_aliases=None, column_major=True,
                         num_non_batch_dims=2, batch_partitionable=True):
  # A lightweight wrapper around ffi.ffi_lowering that can automatically set
  # the layouts appropriately for column-major matrices, which most handlers
  # used here will expect.
  def rule(ctx, *args, **kwargs):
    avals_in_ = ctx.avals_in if avals_in is None else avals_in
    avals_out_ = ctx.avals_out if avals_out is None else avals_out

    # TODO(danfm): Add support for shape polymorphism and batch partitioning.
    has_dynamic_shape = any(
        not is_constant_shape(aval.shape) for aval in (*avals_in_, *avals_out_))
    batch_partitionable_ = batch_partitionable and not has_dynamic_shape

    max_num_dims = max(len(v.shape) for v in avals_in_)
    ctx = ctx.replace(avals_in=avals_in_, avals_out=avals_out_)
    operand_layouts = [
        _column_major_matrix_layout(len(aval.shape))
        if column_major and len(aval.shape) == max_num_dims else None
        for aval in avals_in_]
    result_layouts = [
        _column_major_matrix_layout(len(aval.shape))
        if column_major and len(aval.shape) == max_num_dims else None
        for aval in avals_out_]
    num_batch_dims = max_num_dims - num_non_batch_dims
    frontend_attrs = mlir.ir_attribute({"num_batch_dims": str(num_batch_dims)})
    if batch_partitionable_:
      extra_attributes = {"mhlo.frontend_attributes": frontend_attrs}
      if config.use_shardy_partitioner.value:
        extra_attributes["sdy.sharding_rule"] = _build_sdy_sharding_rule(
            ctx.module_context, num_batch_dims, avals_in_, avals_out_)
    else:
      extra_attributes = None
    rule = ffi.ffi_lowering(target_name, operand_layouts=operand_layouts,
                            result_layouts=result_layouts,
                            operand_output_aliases=operand_output_aliases,
                            extra_attributes=extra_attributes)
    return rule(ctx, *args, **kwargs)
  return rule

