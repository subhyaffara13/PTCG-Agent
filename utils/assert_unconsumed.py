
def assert_unconsumed(key):
  """Assert that a key is unconsumed"""
  assert_consumed_value_p.bind(key, value=HashableArray(False))

