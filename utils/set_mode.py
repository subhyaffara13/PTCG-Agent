
def set_mode(override: BackendMode):
  """Sets global io mode.
  Args:
    override: BackendMode enum value to set for IO mode.
  """
  global io_mode
  io_mode = override

