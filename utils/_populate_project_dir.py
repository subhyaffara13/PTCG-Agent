
def _populate_project_dir(root, files, options):
    # NOTE: Currently pypa/build will refuse to build the project if no
    # `pyproject.toml` or `setup.py` is found. So it is impossible to do
    # completely "config-less" projects.
    basic = {
        "setup.py": "import setuptools\nsetuptools.setup()",
        "README.md": "# Example Package",
        "LICENSE": "Copyright (c) 2018",
    }
    jaraco.path.build(basic, prefix=root)
    _write_setupcfg(root, options)
    paths = (root / f for f in files)
    for path in paths:
        path.parent.mkdir(exist_ok=True, parents=True)
        path.touch()

