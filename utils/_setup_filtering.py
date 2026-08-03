import os

def _setup_filtering(argv: abc.MutableSequence[str]) -> bool:
  """Implements the bazel test filtering protocol.

  The following environment variable is used in this method:

    TESTBRIDGE_TEST_ONLY: string, if set, is forwarded to the unittest
      framework to use as a test filter. Its value is split with shlex, then:
      1. On Python 3.6 and before, split values are passed as positional
         arguments on argv.
      2. On Python 3.7+, split values are passed to unittest's `-k` flag. Tests
         are matched by glob patterns or substring. See
         https://docs.python.org/3/library/unittest.html#cmdoption-unittest-k

  Args:
    argv: the argv to mutate in-place.

  Returns:
    Whether test filtering is requested.
  """
  test_filter = os.environ.get('TESTBRIDGE_TEST_ONLY')
  if argv is None or not test_filter:
    return False

  filters = ['-k=' + test_filter for test_filter in shlex.split(test_filter)]

  argv[1:1] = filters
  return True

