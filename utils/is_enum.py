
def is_enum(node: nodes.ClassDef) -> bool:
    return node.name == "Enum" and node.root().name == "enum"  # type: ignore[no-any-return]

