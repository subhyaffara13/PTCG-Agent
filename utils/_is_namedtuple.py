
def _is_namedtuple(x):
  """Duck typing test for namedtuple factory-generated objects."""
  return isinstance(x, tuple) and hasattr(x, '_fields')


def _is_namedtuple(t):
  return issubclass(t, tuple) and hasattr(t, '_fields')


def _is_namedtuple(obj: Any) -> bool:
    """Checks if an object is most likely a namedtuple. It is possible
    to craft an object that passes this check and isn't a namedtuple, but
    there is only a minuscule chance of this happening unintentionally.

    Args:
        obj (Any): The object to test

    Returns:
        bool: True if the object is a namedtuple. False otherwise.
    """
    try:
        fields = getattr(obj, "_fields", None)
    except Exception:
        # Being very defensive - if we cannot get the attr then its not a namedtuple
        return False
    return isinstance(obj, tuple) and isinstance(fields, tuple)


def _is_namedtuple(obj: Any) -> bool:
    # Check if type was created from collections.namedtuple or a typing.NamedTuple.
    return (
        isinstance(obj, tuple) and hasattr(obj, "_asdict") and hasattr(obj, "_fields")
    )


def _is_namedtuple(obj: Any) -> bool:
    # Mirrors torch.nn.parallel.scatter_gather._is_namedtuple
    fields = getattr(type(obj), "_fields", None)
    return (
        isinstance(obj, tuple)
        and hasattr(obj, "_asdict")
        and isinstance(fields, tuple)
        and all(isinstance(f, str) for f in fields)
    )


def _is_namedtuple(obj: Any) -> bool:
    """Checks if an object is most likely a namedtuple. It is possible
    to craft an object that passes this check and isn't a namedtuple, but
    there is only a minuscule chance of this happening unintentionally.

    Args:
        obj (Any): The object to test

    Returns:
        bool: True if the object is a namedtuple. False otherwise.
    """
    try:
        fields = getattr(obj, "_fields", None)
    except Exception:
        # Being very defensive - if we cannot get the attr then its not a namedtuple
        return False
    return isinstance(obj, tuple) and isinstance(fields, tuple)


def _is_namedtuple(nodetype: type) -> bool:
  return (issubclass(nodetype, tuple) and
          hasattr(nodetype, "_fields") and
          isinstance(nodetype._fields, Sequence) and
          all(isinstance(f, str) for f in nodetype._fields))

