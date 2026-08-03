from pathlib import Path


def get_testdir():
    testroot = Path(__file__).resolve().parent / "src"
    return testroot / "array_from_pyobj"

