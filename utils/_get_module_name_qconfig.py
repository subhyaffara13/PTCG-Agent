
def _get_module_name_qconfig(qconfig_mapping, module_name, fallback_qconfig):
    if module_name == "":
        # module name qconfig not found
        return fallback_qconfig
    if module_name in qconfig_mapping.module_name_qconfigs:
        return qconfig_mapping.module_name_qconfigs[module_name]
    else:
        parent, _ = _parent_name(module_name)
        return _get_module_name_qconfig(qconfig_mapping, parent, fallback_qconfig)

