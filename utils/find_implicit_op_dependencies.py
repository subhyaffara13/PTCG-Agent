
def find_implicit_op_dependencies(fn: FuncIR) -> set[Dependency] | None:
    """Find implicit dependencies that need to be imported.

    Using primitives or types defined in librt submodules such as "librt.base64"
    requires dependency imports (e.g., capsule imports).

    Note that a module can depend on a librt module even if it doesn't explicitly
    import it, for example via re-exported names or via return types of functions
    defined in other modules.
    """
    deps: set[Dependency] | None = None
    # Check function signature types for dependencies
    deps = find_type_dependencies(fn, deps)
    # Check ops for dependencies
    for block in fn.blocks:
        for op in block.ops:
            assert not isinstance(op, PrimitiveOp), "Lowered IR is expected"
            if isinstance(op, CallC) and op.dependencies is not None:
                for dep in op.dependencies:
                    if deps is None:
                        deps = set()
                    deps.add(dep)
            deps = collect_type_deps(op.type, deps)
            if isinstance(op, Assign):
                deps = collect_type_deps(op.dest.type, deps)
    return deps

