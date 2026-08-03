import os

def static_bool_env(varname: str, default: bool) -> bool:
  """Read an environment variable and interpret it as a boolean.

  This is deprecated. Please use bool_flag() unless your flag
  will be used in a static method and does not require runtime updates.

  True values are (case insensitive): 'y', 'yes', 't', 'true', 'on', and '1';
  false values are 'n', 'no', 'f', 'false', 'off', and '0'.
  Args:
    varname: the name of the variable
    default: the default boolean value
  Returns:
    boolean return value derived from defaults and environment.
  Raises: ValueError if the environment variable is anything else.
  """
  val = os.getenv(varname, str(default))
  val = val.lower()
  if val in ('y', 'yes', 't', 'true', 'on', '1'):
    return True
  elif val in ('n', 'no', 'f', 'false', 'off', '0'):
    return False
  else:
    raise ValueError(
      f'invalid truth value {val!r} for environment {varname!r}'
    )

