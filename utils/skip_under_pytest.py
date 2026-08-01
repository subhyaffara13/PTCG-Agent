
def skip_under_pytest(reason: str):
  """A decorator for test methods to skip the test when run under pytest."""
  reason = "Running under pytest: " + reason
  def skip(test_method):
    return unittest.skipIf(is_running_under_pytest(), reason)(test_method)
  return skip

