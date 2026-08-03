from typing import Any

def _private_setattr_handler(model: BaseModel, name: str, val: Any) -> None:
    if getattr(model, '__pydantic_private__', None) is None:
        # While the attribute should be present at this point, this may not be the case if
        # users do unusual stuff with `model_post_init()` (which is where the  `__pydantic_private__`
        # is initialized, by wrapping the user-defined `model_post_init()`), e.g. if they mock
        # the `model_post_init()` call. Ideally we should find a better way to init private attrs.
        object.__setattr__(model, '__pydantic_private__', {})
    model.__pydantic_private__[name] = val  # pyright: ignore[reportOptionalSubscript]

