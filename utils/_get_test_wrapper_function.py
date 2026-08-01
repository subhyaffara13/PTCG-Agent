
def _get_test_wrapper_function(test_func):
  """Creates a function to wrap a test method with custom patches."""

  def test_wrapper(self, *args, **kwargs):

    def _get_unique_barrier_key(key: str) -> str:
      return f'{key}.{self.id()}'

    with mock.patch.object(
        multihost,
        '_unique_barrier_key',
        new=_get_unique_barrier_key,
    ):
      return test_func(self, *args, **kwargs)

  return test_wrapper

