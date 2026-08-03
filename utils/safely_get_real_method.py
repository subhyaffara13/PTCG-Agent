from typing import Any, Callable

def safely_get_real_method(
    obj: Any, method_name: str
) -> Callable[..., Any] | None:
  """Safely retrieves a method directly implemented on a type.

  This function can be used to safely retrieve a "real" method from an object,
  e.g. a method that is actually defined on the object or a superclass. This
  can be used to avoid accidentally trying to call special methods on proxy
  objects or other objects that override `__getattr__`.

  Args:
    obj: The object to retrieve the method from.
    method_name: The name of the method to retrieve.

  Returns:
    The method if it is found, or None if it is not found.
  """
  if not hasattr(type(obj), method_name) or not hasattr(obj, method_name):
    return None

  try:
    retrieved = getattr(obj, method_name)
    if not isinstance(retrieved, types.MethodType):
      return None
    return retrieved
  except Exception:  # pylint: disable=broad-exception-caught
    return None

