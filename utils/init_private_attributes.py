from typing import Any

def init_private_attributes(self: BaseModel, context: Any, /) -> None:
    """This function is meant to behave like a BaseModel method to initialize private attributes.

    It takes context as an argument since that's what pydantic-core passes when calling it.

    Args:
        self: The BaseModel instance.
        context: The context.
    """
    if getattr(self, '__pydantic_private__', None) is None:
        pydantic_private = {}
        for name, private_attr in self.__private_attributes__.items():
            # Avoid needlessly creating a new dict for the validated data:
            if private_attr.default_factory_takes_validated_data:
                default = private_attr.get_default(
                    call_default_factory=True, validated_data={**self.__dict__, **pydantic_private}
                )
            else:
                default = private_attr.get_default(call_default_factory=True)
            if default is not PydanticUndefined:
                pydantic_private[name] = default
        object_setattr(self, '__pydantic_private__', pydantic_private)

