
def _capture_output(fp: TextIO) -> Generator[Callable[[], str], None, None]:
  """Context manager to capture all output written to a given file object.

  Unlike ``contextlib.redirect_stdout``, this context manager works for
  any file object and also for both pure Python and native code.

  Example::

    with capture_output(sys.stdout) as get_output:
      print(42)
    print("Captured": get_output())

  Yields:
    A function returning the captured output. The function must be called
    *after* the context is no longer active.
  """
  # ``None`` means nothing has not been captured yet.
  captured = None

  def get_output() -> str:
    if captured is None:
      raise ValueError("get_output() called while the context is active.")
    return captured

  with tempfile.NamedTemporaryFile(mode="w+", encoding='utf-8') as f:
    original_fd = os.dup(fp.fileno())
    os.dup2(f.fileno(), fp.fileno())
    try:
      yield get_output
    finally:
      # Python also has its own buffers, make sure everything is flushed.
      fp.flush()
      os.fsync(fp.fileno())
      f.seek(0)
      captured = f.read()
      os.dup2(original_fd, fp.fileno())
      os.close(original_fd)

