from typing import Any

def as_validated_field(validator: Validator_T):
    """
    Decorates a validator function as a [`validated_field`] (i.e. a dataclass field with a custom validator).

    Args:
        validator (`Callable`):
            A method that takes a value as input and raises ValueError/TypeError if the value is invalid.
    """

    def _inner(
        default: Any = MISSING,
        default_factory: Any = MISSING,
        init: bool = True,
        repr: bool = True,
        hash: bool | None = None,
        compare: bool = True,
        metadata: dict | None = None,
        **kwargs: Any,
    ):
        return validated_field(
            validator,
            default=default,
            default_factory=default_factory,
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            metadata=metadata,
            **kwargs,
        )

    return _inner

