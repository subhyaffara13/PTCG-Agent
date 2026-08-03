from typing import Any

def _validate_list(name: str, value: Any, args: tuple[Any, ...]) -> None:
    """Validate list[T] type."""
    if not isinstance(value, list):
        raise TypeError(f"Field '{name}' expected a list, got {type(value).__name__}")

    # Validate each item in the list
    item_type = args[0]
    for i, item in enumerate(value):
        try:
            type_validator(f"{name}[{i}]", item, item_type)
        except TypeError as e:
            raise TypeError(f"Invalid item at index {i} in list '{name}'") from e

