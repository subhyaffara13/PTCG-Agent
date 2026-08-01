
def set_attribute_for_modules(module: nn.Module, key: str, value: Any):
    """
    Set a value to a module and all submodules.
    """
    setattr(module, key, value)
    for submodule in module.children():
        set_attribute_for_modules(submodule, key, value)

