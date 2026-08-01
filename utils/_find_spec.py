
def _find_spec(module_name: str, module_path: StrPath | None) -> ModuleSpec:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    spec = spec or importlib.util.find_spec(module_name)

    if spec is None:
        raise ModuleNotFoundError(module_name)

    return spec


def _find_spec(env_id: str) -> EnvSpec:
    # For string id's, load the environment spec from the registry then make the environment spec
    assert isinstance(env_id, str)

    # The environment name can include an unloaded module in "module:env_name" style
    module, env_name = (None, env_id) if ":" not in env_id else env_id.split(":")
    if module is not None:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(
                f"{e}. Environment registration via importing a module failed. "
                f"Check whether '{module}' contains env registration and can be imported."
            ) from e

    # load the env spec from the registry
    env_spec = registry.get(env_name)

    # update env spec is not version provided, raise warning if out of date
    ns, name, version = parse_env_id(env_name)

    latest_version = find_highest_version(ns, name)
    if version is not None and latest_version is not None and latest_version > version:
        logger.deprecation(
            f"The environment {env_name} is out of date. You should consider "
            f"upgrading to version `v{latest_version}`."
        )
    if version is None and latest_version is not None:
        version = latest_version
        new_env_id = get_env_id(ns, name, version)
        env_spec = registry.get(new_env_id)
        logger.warn(
            f"Using the latest versioned environment `{new_env_id}` "
            f"instead of the unversioned environment `{env_name}`."
        )

    if env_spec is None:
        _check_version_exists(ns, name, version)
        raise error.Error(
            f"No registered env with id: {env_name}. Did you register it, or import the package that registers it? Use `gymnasium.pprint_registry()` to see all of the registered environments."
        )

    return env_spec


def _find_spec(
    module_path: tuple[str, ...], path: tuple[str, ...] | None
) -> ModuleSpec:
    _path = path or sys.path

    # Need a copy for not mutating the argument.
    modpath = list(module_path)

    search_paths = None
    processed: list[str] = []

    while modpath:
        modname = modpath.pop(0)

        submodule_path = search_paths or path
        if submodule_path is not None:
            submodule_path = tuple(submodule_path)

        finder, spec = _find_spec_with_path(
            _path, modname, module_path, tuple(processed), submodule_path
        )
        processed.append(modname)
        if modpath:
            if isinstance(finder, Finder):
                search_paths = finder.contribute_to_path(spec, processed)
            # If modname is a package from an editable install, update search_paths
            # so that the next module in the path will be found inside of it using importlib.
            # Existence of __name__ is guaranteed by _find_spec_with_path.
            elif finder.__name__ in _EditableFinderClasses:  # type: ignore[attr-defined]
                search_paths = spec.submodule_search_locations

        if spec.type == ModuleType.PKG_DIRECTORY:
            spec = spec._replace(submodule_search_locations=search_paths)

    return spec

