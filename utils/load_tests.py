
def load_tests(loader, tests, pattern):
    set_running_script_path()
    test_suite = unittest.TestSuite()
    for test_group in tests:
        if not DISABLE_RUNNING_SCRIPT_CHK:
            for test in test_group:
                check_test_defined_in_running_script(test)
        if test_group._tests:
            test_suite.addTest(test_group)
    return test_suite


def load_tests(loader, tests, ignore):
  del loader, ignore  # Unused.
  tests.addTests(
      doctest.DocTestSuite(
          _ranking, globs={"jax": jax, "jnp": jnp, "optax": optax}
      )
  )
  return tests


def load_tests(loader, tests, pattern):  # pylint: disable=invalid-name,g-doc-args
  """Returns Dynamically created TestSuite.

  This creates one TestCase per game to test.

  See https://docs.python.org/2/library/unittest.html#load-tests-protocol.
  """
  del pattern
  tests = tuple(
      loader.loadTestsFromTestCase(test_case_class)
      for test_case_class in _create_test_case_classes())
  return unittest.TestSuite(tests=tests)

