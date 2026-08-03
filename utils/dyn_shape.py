from typing import Any

def dyn_shape(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> None:
    raise DynamicOutputShapeException(func)

