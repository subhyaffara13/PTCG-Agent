
def collect_env_var_references(*, strings: Iterable[str]) -> Set[str]:
    """Union of every ``${NAME}`` reference across a collection of strings."""
    refs: Set[str] = set()
    for s in strings:
        if isinstance(s, str):
            refs |= find_env_var_references(s)
    return refs

