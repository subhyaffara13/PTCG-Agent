
def get_custom_call_name(has_bias, has_dropout, is_bwd, is_fp8=False):
  return _custom_name_maps[(is_bwd, has_dropout, has_bias, is_fp8)]

