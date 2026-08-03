from typing import Any, Callable, Dict

def custom_pydantic_encoder(type_encoders: dict[Any, Callable[[type[Any]], Any]], obj: Any) -> Any:
    warnings.warn(
        '`custom_pydantic_encoder` is deprecated, use `BaseModel.model_dump` instead.',
        category=PydanticDeprecatedSince20,
        stacklevel=2,
    )
    # Check the class type and its superclasses for a matching encoder
    for base in obj.__class__.__mro__[:-1]:
        try:
            encoder = type_encoders[base]
        except KeyError:
            continue

        return encoder(obj)
    else:  # We have exited the for loop without finding a suitable encoder
        return pydantic_encoder(obj)


def custom_pydantic_encoder(type_encoders: Dict[Any, Callable[[Type[Any]], Any]], obj: Any) -> Any:
    # Check the class type and its superclasses for a matching encoder
    for base in obj.__class__.__mro__[:-1]:
        try:
            encoder = type_encoders[base]
        except KeyError:
            continue

        return encoder(obj)
    else:  # We have exited the for loop without finding a suitable encoder
        return pydantic_encoder(obj)

