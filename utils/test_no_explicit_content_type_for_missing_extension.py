
def test_no_explicit_content_type_for_missing_extension(tmp_path):
    pyproject = _pep621_example_project(tmp_path, "README")
    dist = pyprojecttoml.apply_configuration(makedist(tmp_path), pyproject)
    assert dist.metadata.long_description_content_type is None

