
def infer_namespace(node, context: InferenceContext | None = None):
    callsite = arguments.CallSite.from_call(node, context=context)
    if not callsite.keyword_arguments:
        # Cannot make sense of it.
        raise UseInferenceDefault()

    class_node = nodes.ClassDef(
        "Namespace",
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=nodes.SYNTHETIC_ROOT,  # this class is not real
        end_lineno=node.end_lineno,
        end_col_offset=node.end_col_offset,
    )
    for attr in set(callsite.keyword_arguments):
        fake_node = nodes.EmptyNode()
        fake_node.parent = class_node
        fake_node.attrname = attr
        class_node.instance_attrs[attr] = [fake_node]
    return iter((class_node.instantiate_class(),))

