
def dataclass_with_extra(cls: type[T]) -> type[T]:
    """Decorator to add a custom __repr__ method to a dataclass, showing all fields, including extra ones.

    This decorator only works with dataclasses that inherit from `BaseInferenceType`.
    """
    cls = dataclass(cls)
    cls.__repr__ = _repr_with_extra  # type: ignore[method-assign]
    return cls

