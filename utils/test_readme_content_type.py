
def test_readme_content_type(tmp_path, readme, ctype):
    pyproject = _pep621_example_project(tmp_path, readme)
    dist = pyprojecttoml.apply_configuration(makedist(tmp_path), pyproject)
    assert dist.metadata.long_description_content_type == ctype

