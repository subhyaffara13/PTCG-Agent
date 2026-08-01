
def filter_traceback(entry: TracebackEntry) -> bool:
    """Return True if a TracebackEntry instance should be included in tracebacks.

    We hide traceback entries of:

    * dynamically generated code (no code to show up for it);
    * internal traceback from pytest or its internal libraries, py and pluggy.
    """
    # entry.path might sometimes return a str object when the entry
    # points to dynamically generated code.
    # See https://bitbucket.org/pytest-dev/py/issues/71.
    raw_filename = entry.frame.code.raw.co_filename
    is_generated = "<" in raw_filename and ">" in raw_filename
    if is_generated:
        return False

    # entry.path might point to a non-existing file, in which case it will
    # also return a str object. See #1133.
    p = Path(entry.path)

    parents = p.parents
    if _PLUGGY_DIR in parents:
        return False
    if _PYTEST_DIR in parents:
        return False

    return True


def filter_traceback(tb: types.TracebackType) -> types.TracebackType | None:
  out = None
  # Scan the traceback and collect relevant frames.
  frames = list(traceback.walk_tb(tb))
  for f, lineno in reversed(frames):
    if include_frame(f):
      out = types.TracebackType(out, f, f.f_lasti, lineno)
  return out

