
def test_undefined_content_type(tmp_path):
    pyproject = _pep621_example_project(tmp_path, "README.tex")
    with pytest.raises(ValueError, match="Undefined content type for README.tex"):
        pyprojecttoml.apply_configuration(makedist(tmp_path), pyproject)

