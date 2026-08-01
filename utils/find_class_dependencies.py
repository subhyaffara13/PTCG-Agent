
def find_class_dependencies(cl: ClassIR) -> set[Dependency] | None:
    """Find dependencies from class attribute types."""
    deps: set[Dependency] | None = None
    for base in cl.mro:
        for attr_type in base.attributes.values():
            deps = collect_type_deps(attr_type, deps)
    return deps

