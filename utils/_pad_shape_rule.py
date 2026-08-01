
def _pad_shape_rule(operand, padding_value, *, padding_config):
  if np.ndim(padding_value) != 0:
    raise ValueError(f"padding_value must be a scalar; got {np.shape(padding_value)=}")
  op_shape = np.shape(operand)
  if not len(padding_config) == np.ndim(operand):
    raise ValueError("length of padding_config must equal the number of axes "
                     f"of operand, got padding_config {padding_config} "
                     f"for operand shape {op_shape}")
  if not all(i >= 0 for _, _, i in padding_config):
    raise ValueError("interior padding in padding_config must be nonnegative, "
                     f"got padding_config {padding_config}")
  result = tuple(l + h + core.dilate_dim(d, i + 1)
                 for (l, h, i), d in zip(padding_config, op_shape))
  if not all(d >= 0 for d in result):
    msg = (f"Dimension size after padding is not at least 0, "
           f"got result shape {result}, for padding_config {padding_config}"
           f" and operand shape {op_shape}")
    raise ValueError(msg)
  return result

