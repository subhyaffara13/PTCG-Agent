from typing import Any

def resize_as_(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> FakeTensor:
    with in_kernel_invocation_manager(fake_mode):
        return func(*args, **kwargs)

