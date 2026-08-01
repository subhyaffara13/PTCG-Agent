
def test_mixed_dynamic_optional_dependencies(tmp_path):
    """
    Test that if PEP 621 was loosened to allow mixing of dynamic and static
    configurations in the case of fields containing sub-fields (groups),
    things would work out.
    """
    files = {
        "requirements-images.txt": "pillow~=42.0\n  # comment\n",
        "pyproject.toml": cleandoc(
            """
            [project]
            name = "myproj"
            version = "1.0"
            dynamic = ["optional-dependencies"]

            [project.optional-dependencies]
            docs = ["sphinx"]

            [tool.setuptools.dynamic.optional-dependencies.images]
            file = ["requirements-images.txt"]
            """
        ),
    }

    path.build(files, prefix=tmp_path)
    pyproject = tmp_path / "pyproject.toml"
    with pytest.raises(ValueError, match="project.optional-dependencies"):
        apply_configuration(Distribution(), pyproject)

