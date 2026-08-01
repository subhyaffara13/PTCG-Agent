
def _pad_transpose(t, operand, padding_value, *, padding_config):
  if type(t) is ad_util.Zero:
    t_operand = ad_util.Zero(operand.aval) if ad.is_undefined_primal(operand) else None
    t_padv = ad_util.Zero(padding_value.aval) if ad.is_undefined_primal(padding_value) else None
  else:
    lo, hi, interior = util.unzip3(padding_config)
    total = lambda x: reduce_sum(x, list(range(t.ndim)))

    def t_op():
      unpad_config = safe_zip(np.negative(lo), np.negative(hi),
                              np.zeros_like(interior))
      unpadded = pad(t, np.array(0., t.dtype), unpad_config)
      return slicing.slice(unpadded, list(np.zeros_like(lo)), unpadded.shape,
                           list(np.add(interior, 1)))

    t_operand = t_op() if ad.is_undefined_primal(operand) else None
    t_padv = sub(total(t), total(t_operand)) if ad.is_undefined_primal(padding_value) else None
  return [t_operand, t_padv]

