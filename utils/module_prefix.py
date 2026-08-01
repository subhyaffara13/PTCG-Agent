
def module_prefix(modules: Iterable[str], target: str) -> str | None:
    result = split_target(modules, target)
    if result is None:
        return None
    return result[0]

