
def split_target(modules: Iterable[str], target: str) -> tuple[str, str] | None:
    remaining: list[str] = []
    while True:
        if target in modules:
            return target, ".".join(remaining)
        components = target.rsplit(".", 1)
        if len(components) == 1:
            return None
        target = components[0]
        remaining.insert(0, components[1])

