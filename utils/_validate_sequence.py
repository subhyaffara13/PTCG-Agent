
def _validate_sequence(name: str, value: Any, args: tuple[Any, ...]) -> None:
    """Validate Sequence or Sequence[T] type."""
    if not isinstance(value, collections.abc.Sequence):
        raise TypeError(f"Field '{name}' expected a Sequence, got {type(value).__name__}")

    # If no type argument is provided (i.e., just `Sequence`), skip item validation
    if not args:
        return

    # Validate each item in the sequence
    item_type = args[0]
    for i, item in enumerate(value):
        try:
            type_validator(f"{name}[{i}]", item, item_type)
        except TypeError as e:
            raise TypeError(f"Invalid item at index {i} in sequence '{name}'") from e

