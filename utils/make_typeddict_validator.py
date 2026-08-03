from typing import Any, Callable, Dict

def make_typeddict_validator(
    typeddict_cls: Type['TypedDict'], config: Type['BaseConfig']  # type: ignore[valid-type]
) -> Callable[[Any], Dict[str, Any]]:
    from pydantic.v1.annotated_types import create_model_from_typeddict

    TypedDictModel = create_model_from_typeddict(
        typeddict_cls,
        __config__=config,
        __module__=typeddict_cls.__module__,
    )
    typeddict_cls.__pydantic_model__ = TypedDictModel  # type: ignore[attr-defined]

    def typeddict_validator(values: 'TypedDict') -> Dict[str, Any]:  # type: ignore[valid-type]
        return TypedDictModel.parse_obj(values).dict(exclude_unset=True)

    return typeddict_validator

