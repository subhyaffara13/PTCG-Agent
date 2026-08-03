from typing import Any

def _get_local_descriptor_names(
  cls: Any, exclude: Iterable[str] = ()
) -> tuple[str, ...]:
  """Gets descriptor names of a class.

  Args:
    cls: The class to get property names for.
    exclude: Names to exclude from output.

  Returns:
    A list of property names.
  """
  true_properties = set()
  for m, attr in cls.__dict__.items():
    if not callable(attr) and (
      hasattr(attr, '__get__')
      or hasattr(attr, '__set__')
      or hasattr(attr, '__delete__')
    ):
      mtype = type(attr)
      if mtype != staticmethod and mtype != classmethod:
        true_properties.add(m)
  return tuple(true_properties.difference(set(exclude)))

