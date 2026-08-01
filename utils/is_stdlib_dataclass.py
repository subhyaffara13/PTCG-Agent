
def is_stdlib_dataclass(cls: type[Any], /) -> TypeIs[type[StandardDataclass]]:
    """Returns `True` if the class is a stdlib dataclass and *not* a Pydantic dataclass.

    Unlike the stdlib `dataclasses.is_dataclass()` function, this does *not* include subclasses
    of a dataclass that are themselves not dataclasses.

    Args:
        cls: The class.

    Returns:
        `True` if the class is a stdlib dataclass, `False` otherwise.
    """
    return '__dataclass_fields__' in cls.__dict__ and not hasattr(cls, '__pydantic_validator__')

