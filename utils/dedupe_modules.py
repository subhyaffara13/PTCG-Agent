
def dedupe_modules(modules: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[str] = set()
    result = []
    for id, path in modules:
        if id not in seen:
            seen.add(id)
            result.append((id, path))
    return result

