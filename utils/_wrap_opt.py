
def _wrap_opt(opt, wrapper_name, wrapper_kwargs):
  if wrapper_name == 'reduce_on_plateau':
    return combine.chain(opt, contrib.reduce_on_plateau(**wrapper_kwargs))
  return getattr(contrib, wrapper_name)(opt, **wrapper_kwargs)

