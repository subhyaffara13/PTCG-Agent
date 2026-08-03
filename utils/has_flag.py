from typing import Any
from pathlib import Path


def has_flag(compiler: Any, flag: str) -> bool:
    """
    Return the flag if a flag name is supported on the
    specified compiler, otherwise None (can be used as a boolean).
    If multiple flags are passed, return the first that matches.
    """

    with tmp_chdir():
        fname = Path("flagcheck.cpp")
        # Don't trigger -Wunused-parameter.
        fname.write_text("int main (int, char **) { return 0; }", encoding="utf-8")

        try:
            compiler.compile([str(fname)], extra_postargs=[flag])
        except distutils.errors.CompileError:
            return False
        return True


def has_flag(compiler: Any, flag: str) -> bool:
    """
    Return the flag if a flag name is supported on the
    specified compiler, otherwise None (can be used as a boolean).
    If multiple flags are passed, return the first that matches.
    """

    with tmp_chdir():
        fname = Path("flagcheck.cpp")
        # Don't trigger -Wunused-parameter.
        fname.write_text("int main (int, char **) { return 0; }", encoding="utf-8")

        try:
            compiler.compile([str(fname)], extra_postargs=[flag])
        except distutils.errors.CompileError:
            return False
        return True

