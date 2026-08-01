
def find_module_paths_using_search(
    modules: list[str], packages: list[str], search_path: list[str], pyversion: tuple[int, int]
) -> list[StubSource]:
    """Find sources for modules and packages requested.

    This function just looks for source files at the file system level.
    This is used if user passes --no-import, and will not find C modules.
    Exit if some of the modules or packages can't be found.
    """
    result: list[StubSource] = []
    typeshed_path = default_lib_path(mypy.build.default_data_dir(), pyversion, None)
    search_paths = SearchPaths((".",) + tuple(search_path), (), (), tuple(typeshed_path))
    cache = FindModuleCache(search_paths, fscache=None, options=None)
    for module in modules:
        m_result = cache.find_module(module)
        if isinstance(m_result, ModuleNotFoundReason):
            fail_missing(module, m_result)
            module_path = None
        else:
            module_path = m_result
        result.append(StubSource(module, module_path))
    for package in packages:
        p_result = cache.find_modules_recursive(package)
        if p_result:
            fail_missing(package, ModuleNotFoundReason.NOT_FOUND)
        sources = [StubSource(m.module, m.path) for m in p_result]
        result.extend(sources)

    result = [m for m in result if not is_non_library_module(m.module)]

    return result

