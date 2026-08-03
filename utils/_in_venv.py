from pathlib import Path


def _in_venv(path: Path) -> bool:
    """Attempt to detect if ``path`` is the root of a Virtual Environment by
    checking for the existence of the pyvenv.cfg file.

    [https://peps.python.org/pep-0405/]

    For regression protection we also check for conda environments that do not include pyenv.cfg yet --
    https://github.com/conda/conda/issues/13337 is the conda issue tracking adding pyenv.cfg.

    Checking for the `conda-meta/history` file per https://github.com/pytest-dev/pytest/issues/12652#issuecomment-2246336902.

    """
    try:
        return (
            path.joinpath("pyvenv.cfg").is_file()
            or path.joinpath("conda-meta", "history").is_file()
        )
    except OSError:
        return False

