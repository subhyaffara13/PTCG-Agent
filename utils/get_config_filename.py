
def get_config_filename(config_flag) -> str:  # pylint: disable=g-bad-name
  """Returns the path to the config file given the config flag.

  Args:
    config_flag: The flag instance obtained from FLAGS, e.g. FLAGS['config'].

  Returns:
    the path to the config file.
  """
  if not is_config_flag(config_flag):
    raise TypeError('expect a config flag, found {}'.format(type(config_flag)))
  return config_flag.config_filename

