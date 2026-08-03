from typing import Any

def cast_to(
    dtype: torch.dtype, model: torch.fx.GraphModule, inputs: list[Any]
) -> tuple[torch.fx.GraphModule, list[Any]]:
    from torch.utils._pytree import tree_map

    model = model.to(dtype)
    if dtype == torch.float64:
        # If casting to fp64 for accuracy comparison, we need to
        # replace dtype arguments embedded in the graph with fp64
        model = cast_dtype_args_to_fp64(model)

    inputs = tree_map(
        lambda x: x.to(dtype)
        if isinstance(x, torch.Tensor) and x.is_floating_point()
        else x,
        inputs,
    )
    return model, inputs

