
def test_preserve_explicit_name_with_dynamic_version(tmpdir_cwd, monkeypatch):
    """According to #3545 it seems that ``name`` discovery is running,
    even when the project already explicitly sets it.
    This seems to be related to parsing of dynamic versions (via ``attr`` directive),
    which requires the auto-discovery of ``package_dir``.
    """
    files = {
        "src": {
            "pkg": {"__init__.py": "__version__ = 42\n"},
        },
        "pyproject.toml": DALS(
            """
            [project]
            name = "myproj"  # purposefully different from package name
            dynamic = ["version"]
            [tool.setuptools.dynamic]
            version = {"attr" = "pkg.__version__"}
            """
        ),
    }
    jaraco.path.build(files)
    dist = Distribution({})
    orig_analyse_name = dist.set_defaults.analyse_name

    def spy_analyse_name():
        # We can check if name discovery was triggered by ensuring the original
        # name remains instead of the package name.
        orig_analyse_name()
        assert dist.get_name() == "myproj"

    monkeypatch.setattr(dist.set_defaults, "analyse_name", spy_analyse_name)
    dist.parse_config_files()
    assert dist.get_version() == "42"
    assert set(dist.packages) == {"pkg"}

