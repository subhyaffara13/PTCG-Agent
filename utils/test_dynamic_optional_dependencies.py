
def test_dynamic_optional_dependencies(tmp_path):
    files = {
        "requirements-docs.txt": "sphinx\n  # comment\n",
        "pyproject.toml": cleandoc(
            """
            [project]
            name = "myproj"
            version = "1.0"
            dynamic = ["optional-dependencies"]

            [tool.setuptools.dynamic.optional-dependencies.docs]
            file = ["requirements-docs.txt"]

            [build-system]
            requires = ["setuptools", "wheel"]
            build-backend = "setuptools.build_meta"
            """
        ),
    }
    path.build(files, prefix=tmp_path)
    dist = Distribution()
    dist = apply_configuration(dist, tmp_path / "pyproject.toml")
    assert dist.extras_require == {"docs": ["sphinx"]}

