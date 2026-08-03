from typing import Any, Callable

def _validate_outputs(outputs: Any, func: Callable) -> None:
    if isinstance(outputs, Tensor):
        return
    if not isinstance(outputs, tuple):
        raise ValueError(
            f"vmap({_get_name(func)}, ...): `{_get_name(func)}` must only return "
            f"Tensors, got type {type(outputs)} as the return."
        )
    for idx, output in enumerate(outputs):
        if isinstance(output, Tensor):
            continue
        raise ValueError(
            f"vmap({_get_name(func)}, ...): `{_get_name(func)}` must only return "
            f"Tensors, got type {type(output)} for return {idx}."
        )

