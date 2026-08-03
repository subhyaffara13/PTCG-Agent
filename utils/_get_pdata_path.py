from pathlib import Path


def _get_pdata_path(
    base_name: Path, recurs: int, pylint_home: Path = PYLINT_HOME_AS_PATH
) -> Path:
    # We strip all characters that can't be used in a filename. Also strip '/' and
    # '\\' because we want to create a single file, not sub-directories.
    underscored_name = "_".join(
        str(p.replace(":", "_").replace("/", "_").replace("\\", "_"))
        for p in base_name.parts
    )
    return pylint_home / f"{underscored_name}_{recurs}.stats"

