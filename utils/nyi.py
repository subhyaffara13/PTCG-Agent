from typing import Any

def nyi(fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any) -> None:
    if func in _device_not_kwarg_ops:
        raise AssertionError(f"NYI: {func}")

