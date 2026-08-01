
def test_license_classifier_with_license_expression(tmp_path):
    text = PEP639_LICENSE_EXPRESSION.rsplit("\n", 2)[0]
    pyproject = _pep621_example_project(
        tmp_path,
        "README",
        f"{text}\n    \"License :: OSI Approved :: MIT License\"\n]",
    )
    msg = "License classifiers have been superseded by license expressions"
    with pytest.raises(InvalidConfigError, match=msg) as exc:
        pyprojecttoml.apply_configuration(makedist(tmp_path), pyproject)

    assert "License :: OSI Approved :: MIT License" in str(exc.value)

