
def random_fold_in_abstract_eval(keys_aval, msgs_aval):
  shape = lax.broadcasting_shape_rule(
      'random_fold_in', keys_aval, msgs_aval)
  sharding = lax.broadcasting_sharding_rule(
      'random_fold_in', keys_aval, msgs_aval)
  vma = core.standard_vma_rule('random_fold_in', keys_aval, msgs_aval)
  out_mat = core.ManualAxisType(varying=vma)
  return core.ShapedArray(shape, keys_aval.dtype, sharding=sharding,
                          manual_axis_type=out_mat)

