from typing import Any

def _get_local_method_names(
  cls: Any, exclude: Iterable[str] = ()
) -> tuple[str, ...]:
  """Gets method names of a class, excluding class and static methods.

  Args:
    cls: The class to get method names for.
    exclude: Names to exclude from output.

  Returns:
    A list of method names.
  """
  true_methods = set()
  for m in cls.__dict__:
    if callable(cls.__dict__[m]) and not inspect.isclass(
      cls.__dict__[m]
    ):  # pytype: disable=not-supported-yet
      mtype = type(cls.__dict__[m])
      if mtype != staticmethod and mtype != classmethod:
        true_methods.add(m)
  return tuple(true_methods.difference(set(exclude)))

