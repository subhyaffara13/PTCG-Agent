from typing import Any

def _validate_union(name: str, value: Any, args: tuple[Any, ...]) -> None:
    """Validate that value matches one of the types in a Union."""
    errors = []
    for t in args:
        try:
            type_validator(name, value, t)
            return  # Valid if any type matches
        except TypeError as e:
            errors.append(str(e))

    raise TypeError(
        f"Field '{name}' with value {repr(value)} doesn't match any type in {args}. Errors: {'; '.join(errors)}"
    )

