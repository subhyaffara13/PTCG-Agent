import logging
from typing import Any

def _engine_run_backward(
    t_outputs: Sequence[torch.Tensor | GradientEdge],
    *args: Any,
    **kwargs: Any,
) -> tuple[torch.Tensor, ...]:
    attach_logging_hooks = log.getEffectiveLevel() <= logging.DEBUG
    if attach_logging_hooks:
        unregister_hooks = _register_logging_hooks_on_whole_graph(t_outputs)

    # Need to save the context so compiler config will be visible in device threads
    torch._C._stash_obj_in_tls("context", contextvars.copy_context())

    try:
        return Variable._execution_engine.run_backward(  # Calls into the C++ engine to run the backward pass
            t_outputs, *args, **kwargs
        )  # Calls into the C++ engine to run the backward pass
    finally:
        if attach_logging_hooks:
            unregister_hooks()  # type: ignore[possibly-undefined]
        torch._C._stash_obj_in_tls("context", None)

