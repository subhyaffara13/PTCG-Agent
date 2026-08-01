
def expand_modules(
    files_or_modules: Sequence[str],
    source_roots: Sequence[str],
    ignore_list: list[str],
    ignore_list_re: list[Pattern[str]],
    ignore_list_paths_re: list[Pattern[str]],
) -> tuple[dict[str, ModuleDescriptionDict], list[ErrorDescriptionDict]]:
    """Take a list of files/modules/packages and return the list of tuple
    (file, module name) which have to be actually checked.
    """
    result: dict[str, ModuleDescriptionDict] = {}
    errors: list[ErrorDescriptionDict] = []
    path = sys.path.copy()

    for something in files_or_modules:
        basename = os.path.basename(something)
        if _is_ignored_file(
            something, ignore_list, ignore_list_re, ignore_list_paths_re
        ):
            result[something] = {
                "path": something,
                "name": "",
                "isarg": False,
                "basepath": something,
                "basename": "",
                "isignored": True,
            }
            continue
        module_package_path = discover_package_path(something, source_roots)
        additional_search_path = [".", module_package_path, *path]
        if os.path.exists(something):
            # this is a file or a directory
            try:
                modname = ".".join(
                    modutils.modpath_from_file(something, path=additional_search_path)
                )
            except ImportError:
                modname = os.path.splitext(basename)[0]
            if os.path.isdir(something):
                filepath = os.path.join(something, "__init__.py")
            else:
                filepath = something
        else:
            # suppose it's a module or package
            modname = something
            try:
                filepath = modutils.file_from_modpath(
                    modname.split("."), path=additional_search_path
                )
                if filepath is None:
                    continue
            except ImportError as ex:
                errors.append({"key": "fatal", "mod": modname, "ex": ex})
                continue
        filepath = os.path.normpath(filepath)
        modparts = (modname or something).split(".")
        try:
            spec = modutils.file_info_from_modpath(
                modparts, path=additional_search_path
            )
        except ImportError:
            # Might not be acceptable, don't crash.
            is_namespace = not os.path.exists(filepath)
            is_directory = os.path.isdir(something)
        else:
            is_namespace = modutils.is_namespace(spec)
            is_directory = modutils.is_directory(spec)
        if not is_namespace:
            default: ModuleDescriptionDict = {
                "path": filepath,
                "name": modname,
                "isarg": True,
                "basepath": filepath,
                "basename": modname,
                "isignored": False,
            }
            result.setdefault(filepath, default)["isarg"] = True
        has_init = (
            modparts[-1] != "__init__" and os.path.basename(filepath) == "__init__.py"
        )
        if has_init or is_namespace or is_directory:
            for subfilepath in modutils.get_module_files(
                os.path.dirname(filepath) or ".", ignore_list, list_all=is_namespace
            ):
                subfilepath = os.path.normpath(subfilepath)
                if filepath == subfilepath:
                    continue
                if _is_ignored_file(
                    subfilepath, ignore_list, ignore_list_re, ignore_list_paths_re
                ):
                    result[subfilepath] = {
                        "path": subfilepath,
                        "name": "",
                        "isarg": False,
                        "basepath": subfilepath,
                        "basename": "",
                        "isignored": True,
                    }
                    continue

                modpath = _modpath_from_file(
                    subfilepath, is_namespace, path=additional_search_path
                )
                submodname = ".".join(modpath)
                # Preserve arg flag if module is also explicitly given.
                isarg = subfilepath in result and result[subfilepath]["isarg"]
                result[subfilepath] = {
                    "path": subfilepath,
                    "name": submodname,
                    "isarg": isarg,
                    "basepath": filepath,
                    "basename": modname,
                    "isignored": False,
                }
    return result, errors

