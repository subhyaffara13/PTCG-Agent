import copy
from typing import Any

def _unflatten_param_groups(
    state_dict: dict[str, Any],
    param_key_to_param: dict[int | str, nn.Parameter],
    param_to_fqns: dict[nn.Parameter, list[str]],
) -> list[dict[str, Any]]:
    param_groups: list[dict[str, Any]] = []
    for flat_param_group in state_dict["param_groups"]:
        unflat_param_group = copy.deepcopy(flat_param_group)
        param_group_params = [
            param_key_to_param[flat_param_key]
            for flat_param_key in flat_param_group["params"]
        ]
        nested_unflat_param_names = [
            param_to_fqns[param] for param in param_group_params
        ]
        unflat_param_group["params"] = [
            *chain.from_iterable(nested_unflat_param_names)
        ]  # flatten the list of lists
        param_groups.append(unflat_param_group)
    return param_groups

