
def _update_module_param(param_list: list[tuple[nn.Module, str, nn.Parameter]]):
    """
    Update parameters within the module
    """
    for item in param_list:
        parent_module, module_path, t = item
        if not hasattr(parent_module, module_path):
            raise AssertionError
        delattr(parent_module, module_path)
        setattr(parent_module, module_path, t)

