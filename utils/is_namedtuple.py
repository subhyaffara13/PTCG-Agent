from typing import Any

def is_namedtuple(obj: Any, /) -> bool:
    """Return whether the argument is a named tuple type.

    This includes [`NamedTuple`][typing.NamedTuple] subclasses and classes created from the
    [`collections.namedtuple`][] factory function.

    ```pycon
    >>> class User(NamedTuple):
    ...     name: str
    ...
    >>> is_namedtuple(User)
    True
    >>> City = collections.namedtuple('City', [])
    >>> is_namedtuple(City)
    True
    >>> is_namedtuple(NamedTuple)
    False
    ```
    """
    return isinstance(obj, type) and issubclass(obj, tuple) and hasattr(obj, '_fields')  # pyright: ignore[reportUnknownArgumentType]


def is_namedtuple(obj: object | type) -> bool:
    """Return whether the object is an instance of namedtuple or a subclass of namedtuple."""
    cls = obj if isinstance(obj, type) else type(obj)
    return is_namedtuple_class(cls)


def is_namedtuple(obj: Any) -> bool:
    """Test if an object is a namedtuple or a torch.return_types.* quasi-namedtuple"""
    return is_namedtuple_cls(type(obj))


def is_namedtuple(obj: Any) -> bool:
    # Check if type was created from collections.namedtuple or a typing.NamedTuple.
    return _is_namedtuple(obj)


def is_namedtuple(type_: Type[Any]) -> bool:
    """
    Check if a given class is a named tuple.
    It can be either a `typing.NamedTuple` or `collections.namedtuple`
    """
    from pydantic.v1.utils import lenient_issubclass

    return lenient_issubclass(type_, tuple) and hasattr(type_, '_fields')


def is_namedtuple(tp: Any, /) -> bool:
    """Return whether the provided argument is a named tuple class.

    The class can be created using `typing.NamedTuple` or `collections.namedtuple`.
    Parametrized generic classes are *not* assumed to be named tuples.
    """
    from ._utils import lenient_issubclass  # circ. import

    return lenient_issubclass(tp, tuple) and hasattr(tp, '_fields')


def is_namedtuple(instance):
    return isinstance(instance, tuple) and getattr(instance, "_fields", None)


def is_namedtuple(x) -> bool:
  """Returns `True` if the value is instance of `NamedTuple`.

  This is using some heuristic by checking for a `._field` attribute.

  Args:
    x: Object to check

  Returns:
    `True` if the object is a `namedtuple`
  """
  return isinstance(x, tuple) and hasattr(type(x), '_fields')

