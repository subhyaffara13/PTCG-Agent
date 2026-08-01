
def test_license_in_metadata(
    license,
    license_expression,
    content_str,
    not_content_str,
    pyproject_text,
    tmp_path,
):
    pyproject = _pep621_example_project(
        tmp_path,
        "README",
        pyproject_text=pyproject_text,
    )
    dist = pyprojecttoml.apply_configuration(makedist(tmp_path), pyproject)
    assert dist.metadata.license == license
    assert dist.metadata.license_expression == license_expression
    pkg_file = tmp_path / "PKG-FILE"
    with open(pkg_file, "w", encoding="utf-8") as fh:
        dist.metadata.write_pkg_file(fh)
    content = pkg_file.read_text(encoding="utf-8")
    assert "Metadata-Version: 2.4" in content
    assert content_str in content
    assert not_content_str not in content

