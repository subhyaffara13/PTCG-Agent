
def is_sequence(seq):
    if isinstance(seq, str):
        return False
    try:
        len(seq)
    except Exception:
        return False
    return True


def is_sequence(i, include=None):
    """
    Return a boolean indicating whether ``i`` is a sequence in the SymPy
    sense. If anything that fails the test below should be included as
    being a sequence for your application, set 'include' to that object's
    type; multiple types should be passed as a tuple of types.

    Note: although generators can generate a sequence, they often need special
    handling to make sure their elements are captured before the generator is
    exhausted, so these are not included by default in the definition of a
    sequence.

    See also: iterable

    Examples
    ========

    >>> from sympy.utilities.iterables import is_sequence
    >>> from types import GeneratorType
    >>> is_sequence([])
    True
    >>> is_sequence(set())
    False
    >>> is_sequence('abc')
    False
    >>> is_sequence('abc', include=str)
    True
    >>> generator = (c for c in 'abc')
    >>> is_sequence(generator)
    False
    >>> is_sequence(generator, include=(str, GeneratorType))
    True

    """
    return (hasattr(i, '__getitem__') and
            iterable(i) or
            bool(include) and
            isinstance(i, include))


def is_sequence(obj: object) -> bool:
    """
    Check if the object is a sequence of objects.
    String types are not included as sequences here.

    Parameters
    ----------
    obj : The object to check

    Returns
    -------
    is_sequence : bool
        Whether `obj` is a sequence of objects.

    Examples
    --------
    >>> l = [1, 2, 3]
    >>>
    >>> is_sequence(l)
    True
    >>> is_sequence(iter(l))
    False
    """
    try:
        # Can iterate over it.
        iter(obj)  # type: ignore[call-overload]
        # Has a length associated with it.
        len(obj)  # type: ignore[arg-type]
        return not isinstance(obj, (str, bytes))
    except (TypeError, AttributeError):
        return False


def is_sequence(obj: object) -> TypeGuard[Sequence[object]]:
    return isinstance(obj, Sequence)


def is_sequence(type_proto):
    cls_type = type_proto.WhichOneof("value")
    assert cls_type in ["tensor_type", "sequence_type"]
    return cls_type == "sequence_type"


def is_sequence(x: Any) -> bool:
  try:
    iter(x)
  except TypeError:
    return False
  else:
    return True

