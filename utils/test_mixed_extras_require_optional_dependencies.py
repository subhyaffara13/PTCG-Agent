
def test_mixed_extras_require_optional_dependencies(tmp_path):
    files = {
        "pyproject.toml": cleandoc(
            """
            [project]
            name = "myproj"
            version = "1.0"
            optional-dependencies.docs = ["sphinx"]
            """
        ),
    }

    path.build(files, prefix=tmp_path)
    pyproject = tmp_path / "pyproject.toml"

    dist = Distribution({"extras_require": {"hello": ["world"]}})

    with pytest.warns(SetuptoolsWarning, match=".extras_require. overwritten"):
        dist = apply_configuration(dist, pyproject)

    assert dist.extras_require == {"docs": ["sphinx"]}

