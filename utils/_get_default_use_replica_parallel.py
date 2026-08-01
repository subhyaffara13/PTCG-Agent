
def _get_default_use_replica_parallel():
  platform = os.environ.get('JAX_PLATFORMS', '').lower()
  if 'gpu' in platform or 'cuda' in platform:
    return False
  return True

