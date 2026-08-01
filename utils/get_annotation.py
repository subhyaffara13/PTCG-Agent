
def get_annotation(
    node: nodes.AssignAttr | nodes.AssignName,
) -> nodes.Name | nodes.Subscript | None:
    """Return the annotation for `node`."""
    ann = None
    if isinstance(node.parent, nodes.AnnAssign):
        ann = node.parent.annotation
    elif isinstance(node, nodes.AssignAttr):
        init_method = node.parent.parent
        try:
            annotations = dict(zip(init_method.locals, init_method.args.annotations))
            ann = annotations.get(node.parent.value.name)
        except AttributeError:
            pass
    else:
        return ann

    try:
        default, *_ = node.infer()
    except astroid.InferenceError:
        default = ""

    label = get_annotation_label(ann)

    if (
        ann
        and getattr(default, "value", "value") is None
        and not label.startswith("Optional")
        and not (
            isinstance(ann, nodes.BinOp)
            and any(
                isinstance(child, nodes.Const) and child.value is None
                for child in ann.get_children()
            )
        )
    ):
        label = rf"Optional[{label}]"

    if label and ann:
        ann.name = label
    return ann

