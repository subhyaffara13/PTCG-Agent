
def _validate_dict(name: str, value: Any, args: tuple[Any, ...]) -> None:
    """Validate dict[K, V] type."""
    if not isinstance(value, dict):
        raise TypeError(f"Field '{name}' expected a dict, got {type(value).__name__}")

    # Validate keys and values
    key_type, value_type = args
    for k, v in value.items():
        try:
            type_validator(f"{name}.key", k, key_type)
            type_validator(f"{name}[{k!r}]", v, value_type)
        except TypeError as e:
            raise TypeError(f"Invalid key or value in dict '{name}'") from e

