from typing import Any

def _is_safe_to_share(node: Any) -> bool:
  """Returns whether the given node is immutable."""
  # According to the Python data model, "If a class defines mutable objects and
  # implements an __eq__() method, it should not implement __hash__()". So, if
  # we find an object that implements __eq__ and __hash__, we can generally
  # assume it is immutable.
  return (
      type(node).__hash__ is not None
      and type(node).__hash__ is not object.__hash__
      and type(node).__eq__ is not object.__eq__
  ) or type_registries.lookup_immutability_for_type(type(node))

