from typing import Any

def unwrap_batched(args: Any, level: int) -> tuple[Any, Any]:
    flat_args, spec = tree_flatten(args)
    if len(flat_args) == 0:
        return args, ()
    result = [
        (
            torch._C._functorch._unwrap_batched(arg, level)
            if isinstance(arg, torch.Tensor)
            else (arg, None)
        )
        for arg in flat_args
    ]
    output, bdims = zip(*result)
    return tree_unflatten(output, spec), tree_unflatten(bdims, spec)

