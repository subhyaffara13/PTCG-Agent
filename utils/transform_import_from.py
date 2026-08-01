
def transform_import_from(builder: IRBuilder, node: ImportFrom) -> None:
    if node.is_mypy_only:
        return

    module_state = builder.graph[builder.module_name]
    if builder.module_path.endswith("__init__.py"):
        module_package = builder.module_name
    elif module_state.ancestors is not None and module_state.ancestors:
        module_package = module_state.ancestors[0]
    else:
        module_package = ""

    id = importlib.util.resolve_name("." * node.relative + node.id, module_package)
    builder.imports[id] = None

    names = [name for name, _ in node.names]
    as_names = [as_name or name for name, as_name in node.names]

    parent_is_native = builder.is_native_module(id) and builder.is_same_group_module(id)
    transform_import_from_buckets(builder, id, names, as_names, node.line, parent_is_native)

