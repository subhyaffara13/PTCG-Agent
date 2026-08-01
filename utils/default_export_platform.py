
def default_export_platform() -> str:
  """Retrieves the default export platform.

  One of: ``'tpu'``, ``'cpu'``, ``'cuda'``, ``'rocm'``.
  """
  # Canonicalize to turn 'gpu' into 'cuda' or 'rocm'
  return xb.canonicalize_platform(xb.default_backend())

