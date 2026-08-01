
def build_stubs(modules: list[str], options: Options, find_submodules: bool = False) -> list[str]:
    """Uses mypy to construct stub objects for the given modules.

    This sets global state that ``get_stub`` can access.

    Returns all modules we might want to check. If ``find_submodules`` is False, this is equal
    to ``modules``.

    :param modules: List of modules to build stubs for.
    :param options: Mypy options for finding and building stubs.
    :param find_submodules: Whether to attempt to find submodules of the given modules as well.

    """
    data_dir = mypy.build.default_data_dir()
    search_path = mypy.modulefinder.compute_search_paths([], options, data_dir)
    find_module_cache = mypy.modulefinder.FindModuleCache(
        search_path, fscache=None, options=options
    )

    all_modules = []
    sources = []
    for module in modules:
        all_modules.append(module)
        if not find_submodules:
            module_path = find_module_cache.find_module(module)
            if not isinstance(module_path, str):
                # test_module will yield an error later when it can't find stubs
                continue
            sources.append(mypy.modulefinder.BuildSource(module_path, module, None))
        else:
            found_sources = find_module_cache.find_modules_recursive(module)
            sources.extend(found_sources)
            # find submodules via mypy
            all_modules.extend(s.module for s in found_sources if s.module not in all_modules)
            # find submodules via pkgutil
            try:
                runtime = silent_import_module(module)
                all_modules.extend(
                    m.name
                    for m in pkgutil.walk_packages(runtime.__path__, runtime.__name__ + ".")
                    if m.name not in all_modules
                )
            except KeyboardInterrupt:
                raise
            except BaseException:
                pass

    if sources:
        try:
            res = mypy.build.build(sources=sources, options=options)
        except mypy.errors.CompileError as e:
            raise StubtestFailure(f"failed mypy compile:\n{e}") from e
        if res.errors:
            raise StubtestFailure("mypy build errors:\n" + "\n".join(res.errors))

        global _all_stubs
        _all_stubs = res.files

    return all_modules

