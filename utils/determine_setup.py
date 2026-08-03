import os
from pathlib import Path


def determine_setup(
    *,
    inifile: str | None,
    override_ini: Sequence[str] | None,
    args: Sequence[str],
    rootdir_cmd_arg: str | None,
    invocation_dir: Path,
) -> tuple[Path, Path | None, ConfigDict, Sequence[str]]:
    """Determine the rootdir, inifile and ini configuration values from the
    command line arguments.

    :param inifile:
        The `--inifile` command line argument, if given.
    :param override_ini:
        The -o/--override-ini command line arguments, if given.
    :param args:
        The free command line arguments.
    :param rootdir_cmd_arg:
        The `--rootdir` command line argument, if given.
    :param invocation_dir:
        The working directory when pytest was invoked.

    :raises UsageError:
    """
    rootdir = None
    dirs = get_dirs_from_args(args)
    ignored_config_files: Sequence[str] = []

    if inifile:
        inipath_ = absolutepath(inifile)
        inipath: Path | None = inipath_
        inicfg = load_config_dict_from_file(inipath_) or {}
        if rootdir_cmd_arg is None:
            rootdir = inipath_.parent
    else:
        ancestor = get_common_ancestor(invocation_dir, dirs)
        rootdir, inipath, inicfg, ignored_config_files = locate_config(
            invocation_dir, [ancestor]
        )
        if rootdir is None and rootdir_cmd_arg is None:
            for possible_rootdir in (ancestor, *ancestor.parents):
                if (possible_rootdir / "setup.py").is_file():
                    rootdir = possible_rootdir
                    break
            else:
                if dirs != [ancestor]:
                    rootdir, inipath, inicfg, _ = locate_config(invocation_dir, dirs)
                if rootdir is None:
                    rootdir = get_common_ancestor(
                        invocation_dir, [invocation_dir, ancestor]
                    )
                    if is_fs_root(rootdir):
                        rootdir = ancestor
    if rootdir_cmd_arg:
        rootdir = absolutepath(os.path.expandvars(rootdir_cmd_arg))
        if not rootdir.is_dir():
            raise UsageError(
                f"Directory '{rootdir}' not found. Check your '--rootdir' option."
            )

    ini_overrides = parse_override_ini(override_ini)
    inicfg.update(ini_overrides)

    assert rootdir is not None
    return rootdir, inipath, inicfg, ignored_config_files

