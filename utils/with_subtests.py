
def with_subtests(subtests) -> Iterator[None]:
  """Fixture which activate subtests for global usage.

  This fixture is a small wrapper around `subtests` pytest extension fixing
  2 issues:

  * Global usage: https://github.com/pytest-dev/pytest-subtests/issues/44
  * Nested report: https://github.com/pytest-dev/pytest-subtests/issues/45

  Usage:

  ```python
  with_subtests = epy.testing.with_subtests  # Required to register the fixture

  @pytest.mark.usefixtures('with_subtests')
  def my_test():
    with epy.testing.subtest('a'):
      with epy.testing.subtest('b'):
        assert False
  ```

  Args:
    subtests: Subtest fixture

  Yields:
    None
  """
  global _curr_context
  if _curr_context is not None:
    raise AssertionError('Conflicting `subtests` context.')
  new_context = _SubtestContext(subtests=subtests)
  try:
    _curr_context = new_context
    yield
  finally:
    _curr_context = None

