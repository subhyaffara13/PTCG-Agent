
def dataclass_transform(node: nodes.ClassDef) -> nodes.ClassDef | None:
    """Rewrite a dataclass to be easily understood by pylint."""
    node.is_dataclass = True

    for assign_node in _get_dataclass_attributes(node):
        name = assign_node.target.name

        rhs_node = nodes.Unknown(
            lineno=assign_node.lineno,
            col_offset=assign_node.col_offset,
            parent=assign_node,
        )
        rhs_node = AstroidManager().visit_transforms(rhs_node)
        node.instance_attrs[name] = [rhs_node]

    if not _check_generate_dataclass_init(node):
        return None

    kw_only_decorated = False
    if node.decorators.nodes:
        for decorator in node.decorators.nodes:
            if not isinstance(decorator, nodes.Call):
                kw_only_decorated = False
                break
            for keyword in decorator.keywords:
                if keyword.arg == "kw_only":
                    kw_only_decorated = keyword.value.bool_value() is True

    init_str = _generate_dataclass_init(
        node,
        list(_get_dataclass_attributes(node, init=True)),
        kw_only_decorated,
    )

    try:
        init_node = parse(init_str)["__init__"]
    except AstroidSyntaxError:
        pass
    else:
        init_node.parent = node
        init_node.lineno, init_node.col_offset = None, None
        node.locals["__init__"] = [init_node]

        root = node.root()
        if DEFAULT_FACTORY not in root.locals:
            new_assign = parse(f"{DEFAULT_FACTORY} = object()").body[0]
            new_assign.parent = root
            root.locals[DEFAULT_FACTORY] = [new_assign.targets[0]]
    return node

