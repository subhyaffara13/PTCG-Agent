import sys

def python_executable_prefix(v: str) -> list[str]:
    if sys.platform == "win32":
        # on Windows, all Python executables are named `python`. To handle this, there
        # is the `py` launcher, which can be passed a version e.g. `py -3.8`, and it will
        # execute an installed Python 3.8 interpreter. See also:
        # https://docs.python.org/3/using/windows.html#python-launcher-for-windows
        return ["py", f"-{v}"]
    else:
        return [f"python{v}"]

