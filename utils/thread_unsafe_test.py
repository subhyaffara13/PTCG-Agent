
def thread_unsafe_test(condition: bool = True):
  """Decorator for tests that are not thread-safe.

  Args:
    condition: If True, mark the test as thread-unsafe. If False, the test
      runs normally without acquiring the write lock. Defaults to True.

  Note: this decorator (naturally) only applies to what it wraps, not to, say,
  code in separate setUp() or tearDown() methods.
  """
  if TEST_NUM_THREADS.value <= 0 or not condition:
    yield
    return

  _test_rwlock.assert_reader_held()
  _test_rwlock.reader_unlock()
  _test_rwlock.writer_lock()
  try:
    yield
  finally:
    _test_rwlock.writer_unlock()
    _test_rwlock.reader_lock()

