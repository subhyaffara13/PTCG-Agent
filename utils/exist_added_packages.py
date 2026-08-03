import os

def exist_added_packages(suppressed: list[str], manager: BuildManager) -> bool:
    """Find if there are any newly added packages that were previously suppressed.

    Exclude everything not in build for follow-imports=skip.
    """
    for dep in suppressed:
        if dep in manager.source_set.source_modules:
            # We don't need to add any special logic for this. If a module
            # is added to build, importers will be invalidated by normal mechanism.
            continue
        path = find_module_simple(dep, manager)
        if not path:
            continue
        options = manager.options.clone_for_module(dep)
        # Technically this is not 100% correct, since we can have:
        #     from pkg import mod
        # with
        #     [mypy-pkg]
        #     follow-import = silent
        #     [mypy-pkg.mod]
        #     follow-imports = normal
        # But such cases are extremely rare, and this allows us to avoid
        # massive performance impact in much more common situations.
        if options.follow_imports in ("skip", "error") and (
            not path.endswith(".pyi") or options.follow_imports_for_stubs
        ):
            continue
        if os.path.basename(path) in ("__init__.py", "__init__.pyi"):
            return True
    return False

