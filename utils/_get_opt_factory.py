
def _get_opt_factory(opt_name):
  """Get optimizer factory."""
  if hasattr(contrib, opt_name):
    return getattr(contrib, opt_name)
  if hasattr(alias, opt_name):
    return getattr(alias, opt_name)
  raise ValueError(f'Unknown optimizer: {opt_name}')

