from typing import Any

def _validate_set(name: str, value: Any, args: tuple[Any, ...]) -> None:
    """Validate set[T] type."""
    if not isinstance(value, set):
        raise TypeError(f"Field '{name}' expected a set, got {type(value).__name__}")

    # Validate each item in the set
    item_type = args[0]
    for i, item in enumerate(value):
        try:
            type_validator(f"{name} item", item, item_type)
        except TypeError as e:
            raise TypeError(f"Invalid item in set '{name}'") from e

