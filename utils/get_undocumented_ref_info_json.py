
def get_undocumented_ref_info_json(
    tree: MypyFile, type_map: dict[Expression, Type]
) -> list[dict[str, object]]:
    visitor = RefInfoVisitor(type_map)
    tree.accept(visitor)
    return visitor.data

