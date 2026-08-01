
def infer_pattern_match(node: nodes.Call, ctx: context.InferenceContext | None = None):
    """Infer re.Pattern and re.Match as classes.

    For PY39+ add `__class_getitem__`.
    """
    class_def = nodes.ClassDef(
        name=node.parent.targets[0].name,
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=node.parent,
        end_lineno=node.end_lineno,
        end_col_offset=node.end_col_offset,
    )
    func_to_add = _extract_single_node(CLASS_GETITEM_TEMPLATE)
    class_def.locals["__class_getitem__"] = [func_to_add]
    return iter([class_def])


def infer_pattern_match(node: nodes.Call, ctx: context.InferenceContext | None = None):
    """Infer regex.Pattern and regex.Match as classes.

    For PY39+ add `__class_getitem__`.
    """
    class_def = nodes.ClassDef(
        name=node.parent.targets[0].name,
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=node.parent,
        end_lineno=node.end_lineno,
        end_col_offset=node.end_col_offset,
    )
    func_to_add = _extract_single_node(CLASS_GETITEM_TEMPLATE)
    class_def.locals["__class_getitem__"] = [func_to_add]
    return iter([class_def])

