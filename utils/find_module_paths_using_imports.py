import sys

def find_module_paths_using_imports(
    modules: list[str], packages: list[str], verbose: bool, quiet: bool
) -> tuple[list[StubSource], list[StubSource]]:
    """Find path and runtime value of __all__ (if possible) for modules and packages.

    This function uses runtime Python imports to get the information.
    """
    with ModuleInspect() as inspect:
        py_modules: list[StubSource] = []
        c_modules: list[StubSource] = []
        found = list(walk_packages(inspect, packages, verbose))
        modules = modules + found
        modules = [
            mod for mod in modules if not is_non_library_module(mod)
        ]  # We don't want to run any tests or scripts
        for mod in modules:
            try:
                result = find_module_path_and_all_py3(inspect, mod, verbose)
            except CantImport as e:
                tb = traceback.format_exc()
                if verbose:
                    sys.stderr.write(tb)
                if not quiet:
                    report_missing(mod, e.message, tb)
                continue
            if not result:
                c_modules.append(StubSource(mod))
            else:
                path, runtime_all = result
                py_modules.append(StubSource(mod, path, runtime_all))
        return py_modules, c_modules

