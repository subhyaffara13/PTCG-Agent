
def sample_product(*args, **kw):
  """Decorator that samples from a cartesian product of test cases.

  Similar to absltest.parameterized.product(), except that it samples from the
  cartesian product rather than returning the whole thing.

  Arguments:
    *args: each positional argument is a list of dictionaries. The entries
      in a dictionary correspond to name=value argument pairs; one dictionary
      will be chosen for each test case. This allows multiple parameters to be
      correlated.
    **kw: each keyword argument is a list of values. One value will be chosen
      for each test case.
  """
  return parameterized.parameters(*sample_product_testcases(*args, **kw))

