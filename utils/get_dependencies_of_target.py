
def get_dependencies_of_target(
    module_id: str,
    module_tree: MypyFile,
    target: Node,
    type_map: dict[Expression, Type],
    python_version: tuple[int, int],
) -> dict[str, set[str]]:
    """Get dependencies of a target -- don't recursive into nested targets."""
    # TODO: Add tests for this function.
    visitor = DependencyVisitor(type_map, python_version, module_tree.alias_deps)
    with visitor.scope.module_scope(module_id):
        if isinstance(target, MypyFile):
            # Only get dependencies of the top-level of the module. Don't recurse into
            # functions.
            for defn in target.defs:
                # TODO: Recurse into top-level statements and class bodies but skip functions.
                if not isinstance(defn, (ClassDef, Decorator, FuncDef, OverloadedFuncDef)):
                    defn.accept(visitor)
        elif isinstance(target, FuncBase) and target.info:
            # It's a method.
            # TODO: Methods in nested classes.
            with visitor.scope.class_scope(target.info):
                target.accept(visitor)
        else:
            target.accept(visitor)
    return visitor.map

