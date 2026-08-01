
def find_highest_version(ns: str | None, name: str) -> int | None:
    """Finds the highest registered version of the environment given the namespace and name in the registry.

    Args:
        ns: The environment namespace
        name: The environment name (id)

    Returns:
        The highest version of an environment with matching namespace and name, otherwise ``None`` is returned.
    """
    version: list[int] = [
        env_spec.version
        for env_spec in registry.values()
        if env_spec.namespace == ns
        and env_spec.name == name
        and env_spec.version is not None
    ]
    return max(version, default=None)


def find_highest_version(ns: Optional[str], name: str) -> Optional[int]:
    version: List[int] = [
        spec_.version
        for spec_ in registry.values()
        if spec_.namespace == ns and spec_.name == name and spec_.version is not None
    ]
    return max(version, default=None)

