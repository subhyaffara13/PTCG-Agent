from typing import Any

def get_arg_value(
    node: torch.fx.Node, arg_number: int, kwarg_name: str | None = None
) -> Any:
    if len(node.args) > arg_number:
        return node.args[arg_number]
    elif kwarg_name is None:
        return None
    else:
        return node.kwargs.get(kwarg_name)

