
def find_type_dependencies(fn: FuncIR, deps: set[Dependency] | None) -> set[Dependency] | None:
    """Find dependencies from RTypes in function signatures.

    Some RTypes (e.g., those for librt types) have associated dependencies
    that need to be imported when the type is used.
    """
    # Check parameter types
    for arg in fn.decl.sig.args:
        deps = collect_type_deps(arg.type, deps)
    # Check return type
    deps = collect_type_deps(fn.decl.sig.ret_type, deps)
    return deps

