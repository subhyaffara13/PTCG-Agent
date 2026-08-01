
def _get_object_type_qconfig(
    qconfig_mapping: QConfigMapping,
    object_type: Callable | str,
    fallback_qconfig: QConfigAny,
) -> QConfigAny:
    return qconfig_mapping.object_type_qconfigs.get(object_type, fallback_qconfig)

