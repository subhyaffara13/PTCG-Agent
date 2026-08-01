
def del_attribute_from_modules(module: nn.Module, key: str):
    """
    Delete a value from a module and all submodules.
    """
    # because we might remove it previously in case it's a shared module, e.g. activation function
    if hasattr(module, key):
        delattr(module, key)

    for submodule in module.children():
        del_attribute_from_modules(submodule, key)

