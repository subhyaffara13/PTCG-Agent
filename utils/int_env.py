
def int_env(varname: str, default: int) -> int:
  """Read an environment variable and interpret it as an integer."""
  return int(os.getenv(varname, str(default)))

