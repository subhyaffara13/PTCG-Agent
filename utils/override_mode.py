
def override_mode(override: BackendMode):
  # pylint: disable=g-doc-return-or-yield
  """Returns a context manager that changes backend IO mode.
  Args:
    override: BackendMode enum value to set IO mode inside context.
  """
  # pylint: enable=g-doc-return-or-yield
  global io_mode
  io_mode_prev = io_mode
  io_mode = override
  try:
    yield
  finally:
    io_mode = io_mode_prev

