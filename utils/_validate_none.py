
def _validate_none(name: str, value: Any) -> None:
    """Validate None type.

    'None' is not a type, it's a special value. Type should be `NoneType` instead.
    But in type annotations 'None' is accepted so we must support it.
    """
    if value is not None:
        raise TypeError(f"Field '{name}' expected None, got {type(value).__name__}")

