from typing import Any

def get_torch_function_mode_stack_at(ind: int) -> Any:
    assert ind < _len_torch_function_stack() and ind >= 0
    return torch._C._get_function_stack_at(ind)

