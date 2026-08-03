from typing import Any

def get_standard_typevars_map(cls: Any) -> dict[TypeVar, Any] | None:
    """Package a generic type's typevars and parametrization (if present) into a dictionary compatible with the
    `replace_types` function. Specifically, this works with standard typing generics and typing._GenericAlias.
    """
    origin = get_origin(cls)
    if origin is None:
        return None
    if not hasattr(origin, '__parameters__'):
        return None

    # In this case, we know that cls is a _GenericAlias, and origin is the generic type
    # So it is safe to access cls.__args__ and origin.__parameters__
    args: tuple[Any, ...] = cls.__args__  # type: ignore
    parameters: tuple[TypeVar, ...] = origin.__parameters__
    return dict(zip(parameters, args))

