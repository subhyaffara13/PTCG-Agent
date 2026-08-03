from pathlib import Path


def get_related_files(
    tested_configuration_file: str | Path, suffix_filter: str
) -> list[Path]:
    """Return all the file related to a test conf file ending with a suffix."""
    conf_path = Path(tested_configuration_file)
    return [
        p
        for p in conf_path.parent.iterdir()
        if str(p.stem).startswith(conf_path.stem) and str(p).endswith(suffix_filter)
    ]

