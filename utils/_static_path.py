
def _static_path() -> epath.Path:
  """Path to the static resources (`.js`, `.css`)."""
  return epath.resource_path('etils.ecolab') / 'inspects' / 'static'

