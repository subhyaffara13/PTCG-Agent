
def is_test() -> bool:
  """Returns True if running in a test environment."""
  return 'TEST_TMPDIR' in os.environ

