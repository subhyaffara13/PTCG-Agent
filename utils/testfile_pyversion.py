
def testfile_pyversion(path: str) -> tuple[int, int]:
    if m := re.search(r"python3([0-9]+)\.test$", path):
        # For older unsupported version like python38,
        # default to that earliest supported version.
        return max((3, int(m.group(1))), defaults.PYTHON3_VERSION_MIN)
    else:
        return defaults.PYTHON3_VERSION_MIN

