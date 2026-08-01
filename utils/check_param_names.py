
def check_param_names(
    names: Sequence[str | None],
    nodes: list[T],
    fail: Callable[[str, T], None],
    description: str = "function definition",
) -> None:
    seen_names: set[str | None] = set()
    for name, node in zip(names, nodes):
        if name is not None and name in seen_names:
            fail(f'Duplicate parameter "{name}" in {description}', node)
            break
        seen_names.add(name)

