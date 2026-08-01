
def test_utf8_maintainer_in_metadata(  # issue-3663
    expected_maintainers_meta_value,
    pyproject_text,
    tmp_path,
):
    pyproject = _pep621_example_project(
        tmp_path,
        "README",
        pyproject_text=pyproject_text,
    )
    dist = pyprojecttoml.apply_configuration(makedist(tmp_path), pyproject)
    assert dist.metadata.maintainer_email == expected_maintainers_meta_value
    pkg_file = tmp_path / "PKG-FILE"
    with open(pkg_file, "w", encoding="utf-8") as fh:
        dist.metadata.write_pkg_file(fh)
    content = pkg_file.read_text(encoding="utf-8")
    assert f"Maintainer-email: {expected_maintainers_meta_value}" in content

