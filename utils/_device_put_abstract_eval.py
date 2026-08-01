
def _device_put_abstract_eval(*xs, devices, srcs, copy_semantics):
  return [update_dp_aval(x, d) for x, d in zip(xs, devices)]

