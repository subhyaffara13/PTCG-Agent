
def _get_padded_spec(arg_info):
  spec = None if arg_info.sharding is None else arg_info.sharding.spec
  ndim = arg_info.ndim
  if spec is None:
    return (None,) * ndim
  assert len(spec) <= ndim
  return spec + (None,) * (ndim - len(spec))

