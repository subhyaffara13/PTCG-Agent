
def _pallas_call_impl(*args, **params):

  # Call the lowering path
  @api.jit(inline=True)
  def _jit_run(*args):
    return pallas_call_p.bind(*args, **params)

  with config.disable_jit(False):
    return _jit_run(*args)

