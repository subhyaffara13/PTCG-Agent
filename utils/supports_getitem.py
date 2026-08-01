
def supports_getitem(value: nodes.NodeNG, node: nodes.NodeNG) -> bool:
    if isinstance(value, nodes.ClassDef):
        if _supports_protocol_method(value, CLASS_GETITEM_METHOD):
            return True
        if is_postponed_evaluation_enabled(node) and is_node_in_type_annotation_context(
            node
        ):
            return True
    return _supports_protocol(value, _supports_getitem_protocol)

