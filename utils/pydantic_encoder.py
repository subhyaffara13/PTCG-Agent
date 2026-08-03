from typing import Any

def pydantic_encoder(obj: Any) -> Any:
    warnings.warn(
        '`pydantic_encoder` is deprecated, use `pydantic_core.to_jsonable_python` instead.',
        category=PydanticDeprecatedSince20,
        stacklevel=2,
    )
    from dataclasses import asdict, is_dataclass

    BaseModel = import_cached_base_model()

    if isinstance(obj, BaseModel):
        return obj.model_dump()
    elif is_dataclass(obj):
        return asdict(obj)  # type: ignore

    # Check the class type and its superclasses for a matching encoder
    for base in obj.__class__.__mro__[:-1]:
        try:
            encoder = ENCODERS_BY_TYPE[base]
        except KeyError:
            continue
        return encoder(obj)
    else:  # We have exited the for loop without finding a suitable encoder
        raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")


def pydantic_encoder(obj: Any) -> Any:
    from dataclasses import asdict, is_dataclass

    from pydantic.v1.main import BaseModel

    if isinstance(obj, BaseModel):
        return obj.dict()
    elif is_dataclass(obj):
        return asdict(obj)

    # Check the class type and its superclasses for a matching encoder
    for base in obj.__class__.__mro__[:-1]:
        try:
            encoder = ENCODERS_BY_TYPE[base]
        except KeyError:
            continue
        return encoder(obj)
    else:  # We have exited the for loop without finding a suitable encoder
        raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")

