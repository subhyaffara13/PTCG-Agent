from typing import Any

def is_empty_container(value: Any) -> bool:
  return (
      isinstance(value, (dict, list, tuple, Mapping))
      or tree_utils.isinstance_of_namedtuple(value)
  ) and not value

