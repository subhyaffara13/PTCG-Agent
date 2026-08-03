from typing import Any

def validate_subgraph_args_types(lifted_args: tuple[Any, ...] | list[Any]):
    allowed_types = (torch.Tensor, int, torch.SymInt)
    if not all(
        isinstance(arg, (torch.Tensor, int, torch.SymInt)) for arg in lifted_args
    ):
        raise AssertionError(
            f"{lifted_args} can only be of {allowed_types} but got {tuple(type(arg) for arg in lifted_args)}"
        )

