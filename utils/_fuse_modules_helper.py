
def _fuse_modules_helper(
    model,
    modules_to_fuse,
    is_qat,
    fuser_func=fuse_known_modules,
    fuse_custom_config_dict=None,
):
    if fuse_custom_config_dict is None:
        fuse_custom_config_dict = {}
    additional_fuser_method_mapping = fuse_custom_config_dict.get(
        "additional_fuser_method_mapping", {}
    )
    mod_list = [_get_module(model, item) for item in modules_to_fuse]

    # Fuse list of modules
    new_mod_list = fuser_func(mod_list, is_qat, additional_fuser_method_mapping)

    # Replace original module list with fused module list
    for i, item in enumerate(modules_to_fuse):
        _set_module(model, item, new_mod_list[i])

