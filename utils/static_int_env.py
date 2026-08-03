import os

def static_int_env(varname: str, default: int | None) -> int | None:
  """Read an environment variable and interpret it as an integer.

  Args:
    varname: the name of the variable
    default: the default integer value
  Returns:
    integer return value derived from defaults and environment.
  Raises: ValueError if the environment variable is not an integer.
  """
  val = os.getenv(varname)
  if val is None:
    return default
  try:
    return int(val)
  except ValueError:
    raise ValueError(
      f'invalid integer value {val!r} for environment {varname!r}'
    ) from None

