from typing import Any

def autograd_function_backward_rewritten(original_backward: Any) -> Any:
    def new_backward(ctx: Any, *grads: Any) -> Any:
        # pyrefly: ignore [bad-assignment]
        grads = [g.contiguous() for g in grads]
        return original_backward(ctx, *grads)

    return new_backward

