
def subtest(name: str) -> Iterator[None]:
  """Contextmanager for a new subtest. To use with `with_subtests` fixture."""
  if not _curr_context:
    raise AssertionError(
        '`epy.testing.subtest` can only be called inside a '
        '`with_subtests` context.'
    )
  name = str(name)
  _curr_context.names.append(name)
  subtest_name = '/'.join(_curr_context.names)
  try:
    with _curr_context.subtests.test(msg=subtest_name):
      yield
  finally:
    out_name = _curr_context.names.pop()
    assert out_name == name  # Sanity check

