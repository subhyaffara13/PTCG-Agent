from typing import Any, Callable, Dict, Tuple

def make_namedtuple_validator(
    namedtuple_cls: Type[NamedTupleT], config: Type['BaseConfig']
) -> Callable[[Tuple[Any, ...]], NamedTupleT]:
    from pydantic.v1.annotated_types import create_model_from_namedtuple

    NamedTupleModel = create_model_from_namedtuple(
        namedtuple_cls,
        __config__=config,
        __module__=namedtuple_cls.__module__,
    )
    namedtuple_cls.__pydantic_model__ = NamedTupleModel  # type: ignore[attr-defined]

    def namedtuple_validator(values: Tuple[Any, ...]) -> NamedTupleT:
        annotations = NamedTupleModel.__annotations__

        if len(values) > len(annotations):
            raise errors.ListMaxLengthError(limit_value=len(annotations))

        dict_values: Dict[str, Any] = dict(zip(annotations, values))
        validated_dict_values: Dict[str, Any] = dict(NamedTupleModel(**dict_values))
        return namedtuple_cls(**validated_dict_values)

    return namedtuple_validator

