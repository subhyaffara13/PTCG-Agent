
def collect_header_dependencies(modules: dict[str, ModuleIR], *, internal: bool) -> set[str]:
    """Collect all header dependencies from all modules."""
    header_deps: set[str] = set()
    for module in modules.values():
        for dep in module.dependencies:
            if isinstance(dep, (SourceDep, HeaderDep)):
                if dep.internal == internal:
                    header_deps.add(dep.get_header())
            else:
                capsule_dep = dep.internal_dep() if internal else dep.external_dep()
                header_deps.add(capsule_dep.get_header())
    return header_deps

