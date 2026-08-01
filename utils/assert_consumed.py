
def assert_consumed(key, value=True):
  """Assert that a key is consumed"""
  assert_consumed_value_p.bind(key, value=HashableArray(value))

