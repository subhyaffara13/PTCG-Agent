import os

def _prepare(
    install_requires: _StrOrIter, extras_require: Mapping[str, _StrOrIter]
) -> tuple[list[str], dict[str, list[str]]]:
    """Given values for ``install_requires`` and ``extras_require``
    create modified versions in a way that can be written in ``requires.txt``
    """
    extras = _convert_extras_requirements(extras_require)
    return _move_install_requirements_markers(install_requires, extras)


def _prepare(tmp_path, venv_python, monkeypatch):
    download_path = os.getenv("DOWNLOAD_PATH", str(tmp_path))
    os.makedirs(download_path, exist_ok=True)

    # Environment vars used for building some of the packages
    monkeypatch.setenv("USE_MYPYC", "1")

    yield

    # Let's provide the maximum amount of information possible in the case
    # it is necessary to debug the tests directly from the CI logs.
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Temporary directory:")
    map(print, tmp_path.glob("*"))
    print("Virtual environment:")
    run([venv_python, "-m", "pip", "freeze"])

