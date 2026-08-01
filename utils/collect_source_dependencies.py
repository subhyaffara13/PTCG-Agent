
def collect_source_dependencies(modules: dict[str, ModuleIR]) -> set[SourceDep]:
    """Collect all SourceDep dependencies from all modules."""
    source_deps: set[SourceDep] = set()
    for module in modules.values():
        for dep in module.dependencies:
            if isinstance(dep, SourceDep):
                if dep.internal:
                    source_deps.add(dep)
            elif isinstance(dep, Capsule):
                source_deps.add(dep.internal_dep())
    return source_deps

