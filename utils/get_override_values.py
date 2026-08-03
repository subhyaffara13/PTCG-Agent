from typing import Any, Dict

def get_override_values(config_flag) -> Dict[str, Any]:  # pylint: disable=g-bad-name
  """Returns a flat dict containing overridden values from the config flag.

  Args:
    config_flag: The flag instance obtained from FLAGS, e.g. FLAGS['config'].

  Returns:
    a flat dict containing overridden values from the config flag.
  """
  if not is_config_flag(config_flag):
    raise TypeError('expect a config flag, found {}'.format(type(config_flag)))
  return config_flag.override_values

