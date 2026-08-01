
def _check_dependencies(m):
    dependencies = _load_attr_from_module(m, VAR_DEPENDENCY)

    if dependencies is not None:
        missing_deps = [pkg for pkg in dependencies if not _check_module_exists(pkg)]
        if missing_deps:
            raise RuntimeError(f"Missing dependencies: {', '.join(missing_deps)}")

