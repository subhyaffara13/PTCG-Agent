
def assert_every_n_is_x_apart(testclass, values, n, x):
  # For an array of values which is divided into sub-arrays of size n,
  # asserts that the first element of every group is at least x greater
  # than the last element of the previous group.
  values = sorted(values)
  assert len(values) % n == 0
  for i in range(n, len(values), n):
    testclass.assertGreaterEqual(values[i], values[i - 1] + x)

