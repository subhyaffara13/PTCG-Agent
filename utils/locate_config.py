from pathlib import Path


def locate_config(
    invocation_dir: Path,
    args: Iterable[Path],
) -> tuple[Path | None, Path | None, ConfigDict, Sequence[str]]:
    """Search in the list of arguments for a valid ini-file for pytest,
    and return a tuple of (rootdir, inifile, cfg-dict, ignored-config-files), where
    ignored-config-files is a list of config basenames found that contain
    pytest configuration but were ignored."""
    config_names = [
        "pytest.toml",
        ".pytest.toml",
        "pytest.ini",
        ".pytest.ini",
        "pyproject.toml",
        "tox.ini",
        "setup.cfg",
    ]
    args = [x for x in args if not str(x).startswith("-")]
    if not args:
        args = [invocation_dir]
    found_pyproject_toml: Path | None = None
    ignored_config_files: list[str] = []

    for arg in args:
        argpath = absolutepath(arg)
        for base in (argpath, *argpath.parents):
            for config_name in config_names:
                p = base / config_name
                if p.is_file():
                    if p.name == "pyproject.toml" and found_pyproject_toml is None:
                        found_pyproject_toml = p
                    ini_config = load_config_dict_from_file(p)
                    if ini_config is not None:
                        index = config_names.index(config_name)
                        for remainder in config_names[index + 1 :]:
                            p2 = base / remainder
                            if (
                                p2.is_file()
                                and load_config_dict_from_file(p2) is not None
                            ):
                                ignored_config_files.append(remainder)
                        return base, p, ini_config, ignored_config_files
    if found_pyproject_toml is not None:
        return found_pyproject_toml.parent, found_pyproject_toml, {}, []
    return None, None, {}, []

