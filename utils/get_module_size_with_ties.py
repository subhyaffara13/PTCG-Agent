
def get_module_size_with_ties(
    tied_params,
    module_size,
    module_sizes,
    modules_to_treat,
) -> tuple[int, list[str], list[nn.Module]]:
    """
    Calculate the total size of a module, including its tied parameters.

    Args:
        tied_params (`List[str]`): The list of tied parameters.
        module_size (`int`): The size of the module without tied parameters.
        module_sizes (`Dict[str, int]`): A dictionary mapping each layer name to its size.
        modules_to_treat (`List[Tuple[str, nn.Module]]`): The list of named modules to treat.

    Returns:
        `Tuple[int, List[str], List[nn.Module]]`: The total size of the module, the names of the tied modules, and the
        tied modules.
    """
    if len(tied_params) < 1:
        return module_size, [], []
    tied_module_names = []
    tied_modules = []

    for tied_param in tied_params:
        tied_module_index = [i for i, (n, _) in enumerate(modules_to_treat) if tied_param.startswith(n + ".")][0]
        tied_module_names.append(modules_to_treat[tied_module_index][0])
        tied_modules.append(modules_to_treat[tied_module_index][1])

    module_size_with_ties = module_size
    for tied_param, tied_module_name in zip(tied_params, tied_module_names):
        module_size_with_ties += module_sizes[tied_module_name] - module_sizes[tied_param]

    return module_size_with_ties, tied_module_names, tied_modules

