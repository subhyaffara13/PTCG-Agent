
def merge_dependencies(new_deps: dict[str, set[str]], deps: dict[str, set[str]]) -> None:
    for trigger, targets in new_deps.items():
        deps.setdefault(trigger, set()).update(targets)

