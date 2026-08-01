
def _run_one_test(test: unittest.TestCase, result: ThreadSafeTestResult):
  if getattr(test.__class__, "thread_hostile", False):
    _test_rwlock.writer_lock()
    try:
      test(result)  # pyrefly: ignore[bad-argument-type]
    finally:
      _test_rwlock.writer_unlock()
  else:
    _test_rwlock.reader_lock()
    try:
      test(result)  # pyrefly: ignore[bad-argument-type]
    finally:
      _test_rwlock.reader_unlock()

