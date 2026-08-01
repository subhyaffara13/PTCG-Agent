
def create_example(path, pkg_root):
    files = {
        "pyproject.toml": EXAMPLE,
        "README.md": "hello world",
        "_files": {
            "file.txt": "",
        },
    }
    packages = {
        "pkg": {
            "__init__.py": "",
            "mod.py": "class CustomSdist: pass",
            "__version__.py": "VERSION = (3, 10)",
            "__main__.py": "def exec(): print('hello')",
        },
    }

    assert pkg_root  # Meta-test: cannot be empty string.

    if pkg_root == ".":
        files = {**files, **packages}
        # skip other files: flat-layout will raise error for multi-package dist
    else:
        # Use this opportunity to ensure namespaces are discovered
        files[pkg_root] = {**packages, "other": {"nested": {"__init__.py": ""}}}

    jaraco.path.build(files, prefix=path)

