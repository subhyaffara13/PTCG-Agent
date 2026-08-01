
def _repair_python_full_version(
    env: dict[str, str | AbstractSet[str]],
) -> dict[str, str | AbstractSet[str]]:
    """
    Work around platform.python_version() returning something that is not PEP 440
    compliant for non-tagged Python builds.
    """
    python_full_version = cast("str", env["python_full_version"])
    if python_full_version.endswith("+"):
        env["python_full_version"] = f"{python_full_version}local"
    return env


def _repair_python_full_version(
    env: dict[str, str | AbstractSet[str]],
) -> dict[str, str | AbstractSet[str]]:
    """
    Work around platform.python_version() returning something that is not PEP 440
    compliant for non-tagged Python builds.
    """
    python_full_version = cast("str", env["python_full_version"])
    if python_full_version.endswith("+"):
        env["python_full_version"] = f"{python_full_version}local"
    return env


def _repair_python_full_version(
    env: dict[str, str | AbstractSet[str]],
) -> dict[str, str | AbstractSet[str]]:
    """
    Work around platform.python_version() returning something that is not PEP 440
    compliant for non-tagged Python builds.
    """
    python_full_version = cast("str", env["python_full_version"])
    if python_full_version.endswith("+"):
        env["python_full_version"] = f"{python_full_version}local"
    return env

