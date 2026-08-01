
def uninferable_final_decorators(
    node: nodes.Decorators,
) -> list[nodes.Attribute | nodes.Name | None]:
    """Return a list of uninferable `typing.final` decorators in `node`.

    This function is used to determine if the `typing.final` decorator is used
    with an unsupported Python version; the decorator cannot be inferred when
    using a Python version lower than 3.8.
    """
    decorators = []
    for decorator in getattr(node, "nodes", []):
        import_nodes: tuple[nodes.Import | nodes.ImportFrom] | None = None

        # Get the `Import` node. The decorator is of the form: @module.name
        if isinstance(decorator, nodes.Attribute):
            inferred = safe_infer(decorator.expr)
            if isinstance(inferred, nodes.Module) and inferred.qname() == "typing":
                _, import_nodes = decorator.expr.lookup(decorator.expr.name)

        # Get the `ImportFrom` node. The decorator is of the form: @name
        elif isinstance(decorator, nodes.Name):
            _, import_nodes = decorator.lookup(decorator.name)

        # The `final` decorator is expected to be found in the
        # import_nodes. Continue if we don't find any `Import` or `ImportFrom`
        # nodes for this decorator.
        if not import_nodes:
            continue
        import_node = import_nodes[0]

        if not isinstance(import_node, (nodes.Import, nodes.ImportFrom)):
            continue

        import_names = dict(import_node.names)

        # Check if the import is of the form: `from typing import final`
        is_from_import = ("final" in import_names) and import_node.modname == "typing"

        # Check if the import is of the form: `import typing`
        is_import = ("typing" in import_names) and getattr(
            decorator, "attrname", None
        ) == "final"

        if is_from_import or is_import:
            inferred = safe_infer(decorator)
            if inferred is None or isinstance(inferred, util.UninferableBase):
                decorators.append(decorator)
    return decorators

