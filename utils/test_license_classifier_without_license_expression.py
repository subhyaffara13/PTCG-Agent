
def test_license_classifier_without_license_expression(tmp_path):
    text = """\
    [project]
    name = "spam"
    version = "2020.0.0"
    license = {text = "mit or apache-2.0"}
    classifiers = ["License :: OSI Approved :: MIT License"]
    """
    pyproject = _pep621_example_project(tmp_path, "README", text)

    msg1 = "License classifiers are deprecated(?:.|\n)*MIT License"
    msg2 = ".project.license. as a TOML table is deprecated"
    with (
        pytest.warns(SetuptoolsDeprecationWarning, match=msg1),
        pytest.warns(SetuptoolsDeprecationWarning, match=msg2),
    ):
        dist = pyprojecttoml.apply_configuration(makedist(tmp_path), pyproject)

    # Check license classifier is still included
    assert dist.metadata.get_classifiers() == ["License :: OSI Approved :: MIT License"]

