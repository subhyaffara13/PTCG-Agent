
def get_version_detail(version: str) -> tuple[int, int]:
    # pyrefly: ignore [bad-assignment]
    version = version.split(".")
    if len(version) != 2:
        raise AssertionError(f"Invalid version {version}")
    major, minor = map(int, version)
    return major, minor

