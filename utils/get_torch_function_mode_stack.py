from typing import Any

def get_torch_function_mode_stack() -> list[Any]:
    return [
        get_torch_function_mode_stack_at(i) for i in range(_len_torch_function_stack())
    ]

