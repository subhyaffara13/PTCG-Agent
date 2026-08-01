
def test_dynamic_dependencies(tmp_path):
    files = {
        "requirements.txt": "six\n  # comment\n",
        "pyproject.toml": cleandoc(
            """
            [project]
            name = "myproj"
            version = "1.0"
            dynamic = ["dependencies"]

            [build-system]
            requires = ["setuptools", "wheel"]
            build-backend = "setuptools.build_meta"

            [tool.setuptools.dynamic.dependencies]
            file = ["requirements.txt"]
            """
        ),
    }
    path.build(files, prefix=tmp_path)
    dist = Distribution()
    dist = apply_configuration(dist, tmp_path / "pyproject.toml")
    assert dist.install_requires == ["six"]

