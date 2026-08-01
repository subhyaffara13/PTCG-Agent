
def transform_import_all(builder: IRBuilder, node: ImportAll) -> None:
    if node.is_mypy_only:
        return
    builder.gen_import(node.id, node.line)

