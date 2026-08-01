
def attr_attributes_transform(node: nodes.ClassDef) -> None:
    """Given that the ClassNode has an attr decorator,
    rewrite class attributes as instance attributes
    """
    # Astroid can't infer this attribute properly
    # Prevents https://github.com/pylint-dev/pylint/issues/1884
    node.locals["__attrs_attrs__"] = [nodes.Unknown(parent=node)]

    use_bare_annotations = is_decorated_with_attrs(node, NEW_ATTRS_NAMES)
    for cdef_body_node in node.body:
        if not isinstance(cdef_body_node, (nodes.Assign, nodes.AnnAssign)):
            continue
        if isinstance(cdef_body_node.value, nodes.Call):
            if cdef_body_node.value.func.as_string() not in ATTRIB_NAMES:
                continue
        elif not use_bare_annotations:
            continue

        # Skip attributes that are explicitly annotated as class variables
        if isinstance(cdef_body_node, nodes.AnnAssign) and is_class_var(
            cdef_body_node.annotation
        ):
            continue

        targets = (
            cdef_body_node.targets
            if hasattr(cdef_body_node, "targets")
            else [cdef_body_node.target]
        )
        for target in targets:
            rhs_node = nodes.Unknown(
                lineno=cdef_body_node.lineno,
                col_offset=cdef_body_node.col_offset,
                parent=cdef_body_node,
            )
            if isinstance(target, nodes.AssignName):
                # Could be a subscript if the code analysed is
                # i = Optional[str] = ""
                # See https://github.com/pylint-dev/pylint/issues/4439
                node.locals[target.name] = [rhs_node]
                node.instance_attrs[target.name] = [rhs_node]

