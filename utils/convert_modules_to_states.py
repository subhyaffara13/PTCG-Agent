from typing import Any

def convert_modules_to_states(values: Any, module_to_index: dict[int, int]) -> Any:
    """Replace nn.Module instances in a pytree with LeafModuleState objects.

    Args:
        values: A pytree of values that may contain nn.Module instances.
        module_to_index: Mapping from id(module) to its integer index.
    """

    def module_to_state(val: Any) -> Any:
        if isinstance(val, torch.nn.Module):
            return LeafModuleState(
                nn_module_index=module_to_index[id(val)],
                named_parameters=dict(val.named_parameters()),
                named_buffers=dict(val.named_buffers()),
            )
        return val

    return pytree.tree_map(module_to_state, values)

