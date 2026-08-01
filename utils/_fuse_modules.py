
def _fuse_modules(
    model,
    modules_to_fuse,
    is_qat,
    inplace=False,
    fuser_func=fuse_known_modules,
    fuse_custom_config_dict=None,
):
    if not inplace:
        model = copy.deepcopy(model)

    if all(isinstance(module_element, str) for module_element in modules_to_fuse):
        # Handle case of modules_to_fuse being a list
        _fuse_modules_helper(
            model, modules_to_fuse, is_qat, fuser_func, fuse_custom_config_dict
        )
    else:
        # Handle case of modules_to_fuse being a list of lists
        for module_list in modules_to_fuse:
            _fuse_modules_helper(
                model, module_list, is_qat, fuser_func, fuse_custom_config_dict
            )
    return model

