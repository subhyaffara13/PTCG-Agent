
def _maybe_adjust_qconfig_for_module_type_or_name(
    qconfig_mapping, module_type, module_name, global_qconfig
):
    # get qconfig for module_name,
    # fallback to module_name_regex_qconfig, module_type_qconfig,
    # global_qconfig if necessary
    module_type_qconfig = _get_object_type_qconfig(
        qconfig_mapping, module_type, global_qconfig
    )
    module_name_regex_qconfig = _get_module_name_regex_qconfig(
        qconfig_mapping, module_name, module_type_qconfig
    )
    module_name_qconfig = _get_module_name_qconfig(
        qconfig_mapping, module_name, module_name_regex_qconfig
    )
    return module_name_qconfig

