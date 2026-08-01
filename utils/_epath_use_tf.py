
def _epath_use_tf() -> bool:
  return os.environ.get('EPATH_USE_TF', '').lower() not in [
      'false',
      'no',
      'f',
      '0',
  ]

