from typing import Any, Callable

def produce_trampoline_autograd_apply(fn_cls: Any) -> Callable[..., Any]:
    def trampoline_autograd_apply(*args: Any, **kwargs: Any) -> Any:
        return fn_cls.apply(*args, **kwargs)

    # type: ignore[attr-defined]
    trampoline_autograd_apply._origin = produce_trampoline_autograd_apply
    return trampoline_autograd_apply

