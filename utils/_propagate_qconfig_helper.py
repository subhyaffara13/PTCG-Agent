
def _propagate_qconfig_helper(
    module,
    qconfig_dict,
    qconfig_parent=None,
    prefix="",
    prepare_custom_config_dict=None,
):
    r"""This is a helper function for `propagate_qconfig_`

    Args:
        module: input module
        qconfig_dict: dictionary that maps from name of submodule to quantization
                     configuration
        qconfig_parent: quantization config of parent module, we will fallback to
                       this config when there is no specified config for current
                       module
        prefix: corresponding prefix of the current module, used as key in
                qconfig_dict
        prepare_custom_config_dict: dictionary for custom handling of modules
                                    see docs for :func:`~torch.ao.quantization.prepare_fx`

    Return:
        None, module is modified inplace with qconfig attached
    """

    module_qconfig = qconfig_dict.get(
        type_before_parametrizations(module), qconfig_parent
    )
    module_qconfig = qconfig_dict.get(prefix, module_qconfig)
    module_qconfig = getattr(module, "qconfig", module_qconfig)

    torch.ao.quantization.qconfig._assert_valid_qconfig(module_qconfig, module)

    qconfig_with_device_check = _add_module_to_qconfig_obs_ctr(module_qconfig, module)
    module.qconfig = qconfig_with_device_check

    for name, child in module.named_children():
        module_prefix = prefix + "." + name if prefix else name
        #  do no not propagate qconfig to child if child is non traceable
        if prepare_custom_config_dict is None or not (
            name in prepare_custom_config_dict.get("non_traceable_module_name", [])
            or type(child)
            in prepare_custom_config_dict.get("non_traceable_module_class", [])
        ):
            _propagate_qconfig_helper(
                child, qconfig_dict, qconfig_with_device_check, module_prefix
            )

