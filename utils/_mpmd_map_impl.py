
def _mpmd_map_impl(*args, **params):
  jit_impl = api.jit(functools.partial(mpmd_map_p.bind, **params))
  with config.disable_jit(False):
    return jit_impl(*args)

