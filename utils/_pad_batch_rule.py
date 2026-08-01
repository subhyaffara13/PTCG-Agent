
def _pad_batch_rule(batched_args, batch_dims, *, padding_config):
  operand, padding_value = batched_args
  operand_bdim, padding_value_bdim = batch_dims
  if operand_bdim is None:
    operand_bdim = 0
    operand = broadcast(operand, (padding_value.shape[padding_value_bdim],))

  padding_config = list(padding_config)
  padding_config.insert(operand_bdim, (0, 0, 0))
  if padding_value_bdim is None:
    return pad(operand, padding_value, padding_config), operand_bdim

  assert padding_value_bdim == 0, padding_value_bdim

  x = pad(operand, _zero(operand), padding_config)
  mask = pad(full_like(operand, True, np.bool_), False, padding_config)
  broadcasted_padding = broadcast_in_dim(padding_value, x.shape,
                                         (operand_bdim,))
  return select(mask, x, broadcasted_padding), operand_bdim

