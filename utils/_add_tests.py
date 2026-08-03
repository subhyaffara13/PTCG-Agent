import os

def _add_tests():
  """Adds a test for each playthrough to the test class (above)."""
  test_srcdir = os.environ.get("TEST_SRCDIR", "")
  path = os.path.join(test_srcdir, _DATA_DIR)
  basenames = sorted(os.listdir(path))
  if len(basenames) < 40:
    raise ValueError(f"Playthroughs are missing from {path}")
  for basename in basenames:
    test_name = f"test_playthrough_{basename}"
    test_func = lambda self, basename=basename: self.run_test(path, basename)
    test_func.__name__ = test_name
    setattr(PlaythroughTest, test_name, test_func)

