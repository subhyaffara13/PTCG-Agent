
def test_compatible_with_numpy_configuration(tmp_path):
    files = [
        "dir1/__init__.py",
        "dir2/__init__.py",
        "file.py",
    ]
    _populate_project_dir(tmp_path, files, {})
    dist = Distribution({})
    dist.configuration = object()
    dist.set_defaults()
    assert dist.py_modules is None
    assert dist.packages is None

