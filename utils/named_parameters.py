
def named_parameters(*testcases):
  """A decorator for creating parameterized tests.

  See the module docstring for a usage example. For every parameter tuple
  passed, the first element of the tuple should be a string and will be appended
  to the name of the test method. Each parameter dict passed must have a value
  for the key "testcase_name", the string representation of that value will be
  appended to the name of the test method.

  Args:
    *testcases: Parameters for the decorated method, either a single iterable,
        or a list of tuples or dicts.

  Raises:
    NoTestsError: Raised when the decorator generates no tests.

  Returns:
     A test generator to be handled by TestGeneratorMetaclass.
  """
  return _parameter_decorator(_NAMED, testcases)

