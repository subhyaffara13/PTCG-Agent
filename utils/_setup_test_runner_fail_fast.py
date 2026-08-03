import os

def _setup_test_runner_fail_fast(argv: abc.MutableSequence[str]) -> None:
  """Implements the bazel test fail fast protocol.

  The following environment variable is used in this method:

    TESTBRIDGE_TEST_RUNNER_FAIL_FAST=<1|0>

  If set to 1, --failfast is passed to the unittest framework to return upon
  first failure.

  Args:
    argv: the argv to mutate in-place.
  """

  if argv is None:
    return

  if os.environ.get('TESTBRIDGE_TEST_RUNNER_FAIL_FAST') != '1':
    return

  argv[1:1] = ['--failfast']

