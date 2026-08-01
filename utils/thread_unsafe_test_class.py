
def thread_unsafe_test_class(condition: bool = True):
  """Decorator that marks a TestCase class as thread-hostile.

  Args:
    condition: If True, mark the test class as thread-hostile. If False, the
      test class runs normally. Defaults to True.
  """
  def f(klass):
    assert issubclass(klass, unittest.TestCase), type(klass)
    klass.thread_hostile = condition
    return klass
  return f

