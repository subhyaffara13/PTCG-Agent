
def parameters(*testcases):
  """A decorator for creating parameterized tests.

  See the module docstring for a usage example.

  Args:
    *testcases: Parameters for the decorated method, either a single
        iterable, or a list of tuples/dicts/objects (for tests with only one
        argument).

  Raises:
    NoTestsError: Raised when the decorator generates no tests.

  Returns:
     A test generator to be handled by TestGeneratorMetaclass.
  """
  return _parameter_decorator(_ARGUMENT_REPR, testcases)

