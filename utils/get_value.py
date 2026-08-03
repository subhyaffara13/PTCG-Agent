import functools
from typing import Any

def get_value(config_path: str, config: Any):
  """Gets value of a single field.

  Example usage:
    >>> config = {'a': {'b', {'c', 10}}}
    >>> assert config_path.get_value('a.b.c', config) == 10

  Args:
    config_path: Any string that `split` can process.
    config: A nested datastructure

  Returns:
    The last object when walking config with config_path.

  Raises:
    IndexError: Integer field not found in nested structure.
    KeyError: Non-integer field not found in nested structure.
    ValueError: Empty/invalid config_path after parsing.
  """
  get_item = functools.partial(_get_item_or_attribute, field_path=config_path)
  return functools.reduce(get_item, split(config_path), config)

