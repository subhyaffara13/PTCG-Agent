
def get_parameter(traced, target: str):
    """
    Returns the parameter given by ``target`` if it exists,
    otherwise throws an error.

    See the docstring for ``get_submodule`` for a more detailed
    explanation of this method's functionality as well as how to
    correctly specify ``target``.

    Args:
        target: The fully-qualified string name of the Parameter
            to look for. (See ``get_submodule`` for how to specify a
            fully-qualified string.)

    Returns:
        torch.nn.Parameter: The Parameter referenced by ``target``

    Raises:
        AttributeError: If the target string references an invalid
            path or resolves to something that is not an
            ``nn.Parameter``
    """
    module_path, _, param_name = target.rpartition(".")

    mod: torch.nn.Module = traced.get_submodule(module_path)

    if not hasattr(mod, param_name):
        raise AttributeError(mod._get_name() + " has no attribute `" + param_name + "`")

    param: torch.nn.Parameter = getattr(mod, param_name)

    return param

