
def live_arrays(platform=None):
  """Return all live arrays in the backend for `platform`.

  If platform is None, it is the default backend.
  """
  return xb.get_backend(platform).live_arrays()

