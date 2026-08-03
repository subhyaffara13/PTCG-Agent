from typing import Any, Callable

def find_torch_dispatch_rule(
    op: Any, torch_dispatch_class: type
) -> Callable[..., Any] | None:
    return singleton.find(op.__qualname__).torch_dispatch_rules.find(
        torch_dispatch_class
    )

