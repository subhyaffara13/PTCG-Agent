
def collect_type_deps(typ: RType, deps: set[Dependency] | None) -> set[Dependency] | None:
    """Collect dependencies from an RType, recursively checking compound types."""
    if typ.dependencies is not None:
        for dep in typ.dependencies:
            if deps is None:
                deps = set()
            deps.add(dep)
    if isinstance(typ, RUnion):
        for item in typ.items:
            deps = collect_type_deps(item, deps)
    elif isinstance(typ, RTuple):
        for item in typ.types:
            deps = collect_type_deps(item, deps)
    elif isinstance(typ, RStruct):
        for item in typ.types:
            deps = collect_type_deps(item, deps)
    elif isinstance(typ, RVec):
        deps = collect_type_deps(typ.item_type, deps)
    return deps

