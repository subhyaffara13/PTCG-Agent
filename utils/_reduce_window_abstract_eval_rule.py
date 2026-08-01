
def _reduce_window_abstract_eval_rule(
    *avals,
    jaxpr,
    consts,
    window_dimensions,
    window_strides,
    padding,
    base_dilation,
    window_dilation,
):
  operand_avals, init_val_avals = util.split_list(avals, [len(avals) // 2])
  if any(
      o.dtype != iv.dtype for o, iv in zip(operand_avals, init_val_avals)
  ):
    msg = ("reduce_window got inconsistent dtypes for operands and init_values:"
           " got operand dtypes {} and init_value dtypes {}.")
    raise TypeError(msg.format([o.dtype for o in operand_avals],
                               [iv.dtype for iv in init_val_avals]))
  if any(len(v.shape) != 0 for v in init_val_avals):
    msg = ("reduce_window expected init_values to be scalars but init_values "
           "have shapes {}.")
    raise TypeError(msg.format([v.shape for v in init_val_avals]))
  out_shape = _common_reduce_window_shape_rule(
      operand_avals[0], window_dimensions, window_strides, padding,
      base_dilation, window_dilation)
  out_sharding = reduce_window_sharding_rule(
      operand_avals[0], window_dimensions, window_strides, padding,
      base_dilation, window_dilation)
  vma = core.standard_vma_rule('reduce_window', *operand_avals)
  if any(core.getu(a) or core.getr(a) for a in operand_avals):
    raise NotImplementedError
  return tuple(ShapedArray(out_shape, op.dtype, sharding=out_sharding,
                           manual_axis_type=op.mat.update(varying=vma))
               for op in operand_avals)

