
def get_dependencies(
    target: MypyFile,
    type_map: dict[Expression, Type],
    python_version: tuple[int, int],
    options: Options,
) -> dict[str, set[str]]:
    """Get all dependencies of a node, recursively."""
    visitor = DependencyVisitor(type_map, python_version, target.alias_deps, options)
    target.accept(visitor)
    return visitor.map

