
def _generic_reduce_window_batch_rule(
    batched_args,
    batch_dims,
    *,
    jaxpr,
    consts,
    window_dimensions,
    window_strides,
    padding,
    base_dilation,
    window_dilation,
):
  num_operands = len(batched_args) // 2
  operands, init_values = util.split_list(batched_args, [num_operands])
  operand_bdims, init_value_bdims = util.split_list(batch_dims, [num_operands])

  if any(init_bdim is not None for init_bdim in init_value_bdims):
    raise NotImplementedError("reduce_window batching is not implemented for "
                              "initial values")

  size = next(x.shape[ax] for x, ax in zip(operands, operand_bdims)
              if ax is not None)
  operands = [batching.bdim_at_front(arg, bdim, size)
              for arg, bdim in zip(operands, operand_bdims)]
  window_dimensions = (1,) + window_dimensions
  window_strides = (1,) + window_strides
  padding = ((0, 0),) + padding
  base_dilation = (1,) + base_dilation
  window_dilation = (1,) + window_dilation
  outs = reduce_window_p.bind(
      *(operands + init_values), jaxpr=jaxpr, consts=consts,
      window_dimensions=window_dimensions, window_strides=window_strides,
      padding=padding, base_dilation=base_dilation,
      window_dilation=window_dilation)
  return outs, (0,) * num_operands

