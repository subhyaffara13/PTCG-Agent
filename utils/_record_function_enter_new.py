from typing import Any

def _record_function_enter_new(
    fake_mode: FakeTensorMode, func: OpOverload, name: str, args: object | None = None
) -> Any:
    # Call the real implementation - returns a custom class, not a tensor
    # Just pass through without wrapping
    with in_kernel_invocation_manager(fake_mode):
        return func(name, args)

