
def barrier_compatible_test(cls):
  """A decorator to be used with a test class.

  This is primarily needed when different processes in a multihost test may be
  executing different code. This will cause operation IDs to get out of sync. If
  all processes always execute the same code, this decorator is not needed.

  E.g.

  @barrier_compatible_test
  class MyTest(googletest.TestCase):
    def test_foo(self):
      ...

  The point of this decorator is to modify all functions to mock the private
  method `multihost._unique_barrier_key`, to append the test case name.
  This allows multiple test cases to reuse barrier names that would otherwise
  conflict.

  Args:
    cls: the test class to decorate.

  Returns:
    The decorated class.
  """
  for name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
    if name.startswith('test'):
      setattr(cls, name, _get_test_wrapper_function(func))
  return cls

