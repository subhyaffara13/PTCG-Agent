
def verify_example(config, path, pkg_root):
    pyproject = path / "pyproject.toml"
    pyproject.write_text(tomli_w.dumps(config), encoding="utf-8")
    expanded = expand_configuration(config, path)
    expanded_project = expanded["project"]
    assert read_configuration(pyproject, expand=True) == expanded
    assert expanded_project["version"] == "3.10"
    assert expanded_project["readme"]["text"] == "hello world"
    assert "packages" in expanded["tool"]["setuptools"]
    if pkg_root == ".":
        # Auto-discovery will raise error for multi-package dist
        assert set(expanded["tool"]["setuptools"]["packages"]) == {"pkg"}
    else:
        assert set(expanded["tool"]["setuptools"]["packages"]) == {
            "pkg",
            "other",
            "other.nested",
        }
    assert expanded["tool"]["setuptools"]["include-package-data"] is True
    assert "" in expanded["tool"]["setuptools"]["package-data"]
    assert "*" not in expanded["tool"]["setuptools"]["package-data"]
    assert expanded["tool"]["setuptools"]["data-files"] == [
        ("data", ["_files/file.txt"])
    ]

