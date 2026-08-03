import os
from typing import Any

def _find_config_file(
    stderr: TextIO | None = None,
) -> tuple[MutableMapping[str, Any], dict[str, _INI_PARSER_CALLABLE], str] | None:

    current_dir = os.path.abspath(os.getcwd())

    while True:
        for name in defaults.CONFIG_NAMES + defaults.SHARED_CONFIG_NAMES:
            config_file = os.path.relpath(os.path.join(current_dir, name))
            ret = _parse_individual_file(config_file, stderr)
            if ret is None:
                continue
            return ret

        if any(
            os.path.exists(os.path.join(current_dir, cvs_root)) for cvs_root in (".git", ".hg")
        ):
            break
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break
        current_dir = parent_dir

    for config_file in defaults.USER_CONFIG_FILES:
        ret = _parse_individual_file(config_file, stderr)
        if ret is None:
            continue
        return ret

    return None


def _find_config_file(path: str) -> str | None:
    # on windows if the homedir isn't detected this returns back `~`
    home = os.path.expanduser("~")
    try:
        home_stat = _stat_key(home) if home != "~" else None
    except OSError:  # FileNotFoundError / PermissionError / etc.
        home_stat = None

    dir_stat = _stat_key(path)
    while True:
        for candidate in ("setup.cfg", "tox.ini", ".flake8"):
            cfg = configparser.RawConfigParser()
            cfg_path = os.path.join(path, candidate)
            try:
                cfg.read(cfg_path, encoding="UTF-8")
            except (UnicodeDecodeError, configparser.ParsingError) as e:
                LOG.warning("ignoring unparseable config %s: %s", cfg_path, e)
            else:
                # only consider it a config if it contains flake8 sections
                if "flake8" in cfg or "flake8:local-plugins" in cfg:
                    return cfg_path

        new_path = os.path.dirname(path)
        new_dir_stat = _stat_key(new_path)
        if new_dir_stat == dir_stat or new_dir_stat == home_stat:
            break
        else:
            path = new_path
            dir_stat = new_dir_stat

    # did not find any configuration file
    return None

