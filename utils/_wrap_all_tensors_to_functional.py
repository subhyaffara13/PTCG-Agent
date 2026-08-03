from typing import Any

def _wrap_all_tensors_to_functional(
    tensor_pytree: Any, level: int, *, _python_functionalize: bool = False
) -> Any:
    return tree_map(
        partial(
            lambda x: _maybe_wrap_functional_tensor(
                x, level, _python_functionalize=_python_functionalize
            )
        ),
        tensor_pytree,
    )

