from typing import Any

def nested_tensors_unsupported(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> None:
    raise UnsupportedOperatorException(func)

