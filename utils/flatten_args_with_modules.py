from typing import Any

def flatten_args_with_modules(
    args_kwargs: tuple[Any, ...],
) -> list[Any]:
    def expand_module(x: Any) -> Any:
        if isinstance(x, torch.nn.Module):
            return LeafModuleState(
                nn_module_index=-1,
                named_parameters=dict(x.named_parameters()),
                named_buffers=dict(x.named_buffers()),
            )
        return x

    expanded = pytree.tree_map(expand_module, args_kwargs)
    return pytree.tree_leaves(expanded)

