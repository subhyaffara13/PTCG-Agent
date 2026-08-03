from pathlib import Path


def _cfg_or_ini_has_config(path: Path | str) -> bool:
    parser = configparser.ConfigParser()
    try:
        parser.read(path, encoding="utf-8")
    except configparser.Error:
        return False
    return any(
        section == "pylint" or section.startswith("pylint.")
        for section in parser.sections()
    )

