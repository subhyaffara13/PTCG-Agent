
def recursive_rename(conf, old_name, new_name):
  """Returns copy of conf with old_name recursively replaced by new_name.

  This is not done in place, no changes are made to conf but a new ConfigDict is
  returned with the changes made. This is useful if the name of a parameter has
  been changed in code but you need to load an old config.

  Example usage:
    updated_conf = configdict.recursive_rename(conf, "config", "kwargs")

  Args:
    conf: a ConfigDict which needs updating
    old_name: the name used in the ConfigDict which is out of sync with the code
    new_name: the name used in the code

  Returns:
    A ConfigDict which is a copy of conf but with all instances of old_name
    replaced with new_name.
  """
  new_conf = ConfigDict()
  for name, c in conf.items():
    if isinstance(c, ConfigDict):
      new_c = recursive_rename(c, old_name, new_name)
    else:
      new_c = c
    if name == old_name:
      setattr(new_conf, new_name, new_c)
    else:
      setattr(new_conf, name, new_c)
  return new_conf

