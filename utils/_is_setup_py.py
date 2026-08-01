
def _is_setup_py(path: Path) -> bool:
    if path.name != "setup.py":
        return False
    contents = path.read_bytes()
    return b"setuptools" in contents or b"distutils" in contents

