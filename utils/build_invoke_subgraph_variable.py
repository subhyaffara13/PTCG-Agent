from typing import Any

def build_invoke_subgraph_variable(**options: Any) -> Any:
    from .variables.higher_order_ops import TorchHigherOrderOperatorVariable

    return TorchHigherOrderOperatorVariable.make(
        torch._higher_order_ops.invoke_subgraph,
        **options,
    )

