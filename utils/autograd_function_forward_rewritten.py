from typing import Any, Callable

def autograd_function_forward_rewritten(
    original_forward: Callable[_P, _R],
    original_setup_context: Callable[..., Any],
) -> Callable[..., _R]:
    def new_forward(ctx: Any, *args: _P.args, **kwargs: _P.kwargs) -> _R:
        output = original_forward(*args, **kwargs)
        original_setup_context(ctx, args, output)
        return output

    return new_forward

