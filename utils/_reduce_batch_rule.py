
def _reduce_batch_rule(batched_args, batch_dims, *, computation, jaxpr,
                       dimensions):
  # TODO(mattjj,frostig): use batch_jaxpr, delete computation (assumes poly??)
  num_operands = len(batched_args) // 2
  operands, init_values = split_list(batched_args, [num_operands])
  operand_bdims, init_value_bdims = split_list(batch_dims, [num_operands])
  if all(init_value_bdim is None
         for init_value_bdim in init_value_bdims):
    size = next(x.shape[ax] for x, ax in zip(batched_args, batch_dims)
                if ax is not None)
    operands = [batching.bdim_at_front(arg, bdim, size)
                for arg, bdim in zip(operands, operand_bdims)]
    new_dimensions = [d + 1 for d in dimensions]
    new_operand_bdims = [0] * num_operands
    return reduce_p.bind(*(operands + init_values),
                         computation=computation,
                         dimensions=tuple(new_dimensions),
                         jaxpr=jaxpr), new_operand_bdims
  else:
    raise NotImplementedError  # loop and stack

