from typing import Any

def validated_field(
    validator: list[Validator_T] | Validator_T,
    default: Any = MISSING,
    default_factory: Any = MISSING,
    init: bool = True,
    repr: bool = True,
    hash: bool | None = None,
    compare: bool = True,
    metadata: dict | None = None,
    **kwargs: Any,
) -> Any:
    """
    Create a dataclass field with a custom validator.

    Useful to apply several checks to a field. If only applying one rule, check out the [`as_validated_field`] decorator.

    Args:
        validator (`Callable` or `list[Callable]`):
            A method that takes a value as input and raises ValueError/TypeError if the value is invalid.
            Can be a list of validators to apply multiple checks.
        **kwargs:
            Additional arguments to pass to `dataclasses.field()`.

    Returns:
        A field with the validator attached in metadata
    """
    if not isinstance(validator, list):
        validator = [validator]
    if metadata is None:
        metadata = {}
    metadata["validator"] = validator
    return field(  # type: ignore
        default=default,  # type: ignore [arg-type]
        default_factory=default_factory,  # type: ignore [arg-type]
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        **kwargs,
    )

