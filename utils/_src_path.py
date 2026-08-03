from pathlib import Path


def _src_path(
    name: str,
    config: Config,
    src_paths: Iterable[Path] | None = None,
    prefix: tuple[str, ...] = (),
) -> tuple[str, str] | None:
    if src_paths is None:
        src_paths = config.src_paths

    root_module_name, *nested_module = name.split(".", 1)
    new_prefix = (*prefix, root_module_name)
    namespace = ".".join(new_prefix)

    for src_path in src_paths:
        module_path = (src_path / root_module_name).resolve()
        if not prefix and not module_path.is_dir() and src_path.name == root_module_name:
            module_path = src_path.resolve()
        if nested_module and (
            namespace in config.namespace_packages
            or (
                config.auto_identify_namespace_packages
                and _is_namespace_package(module_path, config.supported_extensions)
            )
        ):
            return _src_path(nested_module[0], config, (module_path,), new_prefix)
        if (
            _is_module(module_path)
            or _is_package(module_path)
            or _src_path_is_module(src_path, root_module_name)
        ):
            return (sections.FIRSTPARTY, f"Found in one of the configured src_paths: {src_path}.")

    return None

