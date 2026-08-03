import os

def get_default_test_srcdir() -> str:
  """Returns default test source dir."""
  return os.environ.get('TEST_SRCDIR', '')

