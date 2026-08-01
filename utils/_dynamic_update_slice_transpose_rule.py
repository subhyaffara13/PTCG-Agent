
def _dynamic_update_slice_transpose_rule(t, operand, update, *start_indices):
  assert all(not ad.is_undefined_primal(x) for x in start_indices)
  if type(t) is ad_util.Zero:
    operand_t = (ad_util.Zero(operand.aval)
                 if ad.is_undefined_primal(operand) else None)
    update_t = (ad_util.Zero(update.aval)
                if ad.is_undefined_primal(update) else None)
  else:
    update_ct_aval = (update.aval if ad.is_undefined_primal(update) else
                      typeof(update).to_ct_aval())
    zeros = lax._zeros(t, shape=update_ct_aval.shape, sharding=update_ct_aval.sharding)
    operand_t = (dynamic_update_slice_p.bind(t, zeros, *start_indices)
                 if ad.is_undefined_primal(operand) else None)
    update_t = (dynamic_slice_p.bind(t, *start_indices, slice_sizes=update_ct_aval.shape)
                if ad.is_undefined_primal(update) else None)
  return [operand_t, update_t] + [None] * len(start_indices)

