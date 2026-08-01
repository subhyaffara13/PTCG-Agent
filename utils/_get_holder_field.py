
def _get_holder_field(config_path: str, config: Any) -> Tuple[Any, str]:
  """Returns the last part config_path and config to allow assignment.

  Example usage:
    >>> config = {'a': {'b', {'c', 10}}}
    >>> holder, lastfield = _get_holder_field('a.b.c', config)
    >>> assert lastfield == 'c'
    >>> assert holder is config['a']['b']
    >>> assert holder[lastfield] == 10

  Args:
    config_path: Any string that `split` can process.
    config: A nested datastructure that can be accessed via
      _get_item_or_attribute

  Returns:
    The penultimate object when walking config with config_path. And the final
    part of the config path.

  Raises:
    IndexError: Integer field not found in nested structure.
    KeyError: Non-integer field not found in nested structure.
    ValueError: Empty/invalid config_path after parsing.
  """
  fields = split(config_path)
  if not fields:
    raise ValueError('Path cannot be empty')
  get_item = functools.partial(_get_item_or_attribute, field_path=config_path)
  holder = functools.reduce(get_item, fields[:-1], config)
  return holder, fields[-1]

