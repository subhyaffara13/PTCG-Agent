
def _maybe_adjust_qconfig_for_module_name_object_type_order(
    qconfig_mapping: QConfigMapping,
    cur_module_path: str,
    cur_object_type: Callable,
    cur_object_type_idx: int,
    fallback_qconfig: QConfigAny,
) -> QConfigAny:
    for (
        module_name,
        object_type,
        index,
    ), qconfig in qconfig_mapping.module_name_object_type_order_qconfigs.items():
        if (
            (module_name == cur_module_path)
            and (object_type == cur_object_type)
            and (index == cur_object_type_idx)
        ):
            return qconfig
    return fallback_qconfig

