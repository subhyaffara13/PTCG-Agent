
def get_attrs(obj):
    """
    Gets all the attributes of an object though its __dict__ or return None
    """
    if type(obj) in builtins_types \
       or type(obj) is type and obj in builtins_types:
        return
    return getattr(obj, '__dict__', None)


def get_attrs(obj: object) -> dict[str, object]:
  """Parse all attributes from an object.

  Limitation:

  * Descriptor will be resolved, so all properties are executed (some can
    have side effects, or take a lot of time to compute)

  Args:
    obj: Object to inspect

  Returns:
    Dict mapping attribute name to values.
  """
  attrs = {}
  # Merge `dir(obj)` with `object.__dir__(obj)` to bypass custom object
  # `__dir__`
  for k in dir(obj) + object.__dir__(obj):
    if k in attrs:
      continue
    try:
      v = getattr(obj, k)
    except Exception as e:  # pylint: disable=broad-except
      v = ExceptionWrapper(e)
    attrs[k] = v

  return attrs

