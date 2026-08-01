
def skip_on_flag(flag_name, skip_value):
  """A decorator for test methods to skip the test when flags are set."""
  def skip(test_method):
    @functools.wraps(test_method)
    def test_method_wrapper(self, *args, **kwargs):
      flag_value = config._read(flag_name)
      if flag_value == skip_value:
        test_name = getattr(test_method, '__name__', '[unknown test]')
        raise unittest.SkipTest(
          f"{test_name} not supported when FLAGS.{flag_name} is {flag_value}")
      return test_method(self, *args, **kwargs)
    return test_method_wrapper
  return skip

