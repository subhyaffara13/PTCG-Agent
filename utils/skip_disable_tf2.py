import os

def skip_disable_tf2() -> Iterator[None]:
  """Set environment variable."""
  # Allow TF to conditionally detect if they are running inside adhoc (fix
  # b/322775800)
  prev_value = os.environ.get('SKIP_DISABLE_TF2')
  try:
    os.environ['SKIP_DISABLE_TF2'] = '1'
    yield
  finally:
    if prev_value is None:
      del os.environ['SKIP_DISABLE_TF2']
    else:
      os.environ['SKIP_DISABLE_TF2'] = prev_value

