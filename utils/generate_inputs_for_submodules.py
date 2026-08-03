import copy
from typing import Any

def generate_inputs_for_submodules(
    model: torch.nn.Module,
    inputs: Sequence[Any],
    target_submodules: Iterable[str],
    deepcopy: bool = False,
) -> dict[str, Any]:
    """
    Generate inputs for targeting submdoules in the given model. Note that if two submodules refer to the same obj, this
    function doesn't work.

    Args:
        model: root model.
        inputs: inputs to the root model.
        target_submodules: submodules that we want to generate inputs for.

    Returns:
        A dict that maps from submodule name to its inputs.
    """

    handles = []
    results = {}
    submodule_to_names = {mod: name for name, mod in model.named_modules()}

    def pre_forward(module, module_inputs):
        results[submodule_to_names[module]] = (
            copy.deepcopy(module_inputs) if deepcopy else module_inputs
        )

    for name, mod in model.named_modules():
        if name in target_submodules:
            if not isinstance(mod, torch.jit.ScriptModule):
                handles.append(mod.register_forward_pre_hook(pre_forward))

    def clean_up_handles():
        for h in handles:
            h.remove()

    try:
        with torch.no_grad():
            model(*inputs)
    except Exception as e:
        clean_up_handles()
        raise e

    clean_up_handles()
    return results

