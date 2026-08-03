from pathlib import Path


def test_include_package_data_in_setuppy(tmp_path):
    """Builds with ``pyproject.toml`` should consider ``include_package_data`` set in
    ``setup.py``.

    See https://github.com/pypa/setuptools/issues/3197#issuecomment-1079023889
    """
    files = {
        "pyproject.toml": "[project]\nname = 'myproj'\nversion='42'\n",
        "setup.py": "__import__('setuptools').setup(include_package_data=False)",
    }
    jaraco.path.build(files, prefix=tmp_path)

    with Path(tmp_path):
        dist = distutils.core.run_setup("setup.py", {}, stop_after="config")

    assert dist.get_name() == "myproj"
    assert dist.get_version() == "42"
    assert dist.include_package_data is False

