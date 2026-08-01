
def dump_all_dependencies(
    modules: dict[str, MypyFile],
    type_map: dict[Expression, Type],
    python_version: tuple[int, int],
    options: Options,
) -> None:
    """Generate dependencies for all interesting modules and print them to stdout."""
    all_deps: dict[str, set[str]] = {}
    for id, node in modules.items():
        # Uncomment for debugging:
        # print('processing', id)
        if id in ("builtins", "typing") or "/typeshed/" in node.path:
            continue
        assert id == node.fullname
        deps = get_dependencies(node, type_map, python_version, options)
        for trigger, targets in deps.items():
            all_deps.setdefault(trigger, set()).update(targets)
    type_state.add_all_protocol_deps(all_deps)

    for trigger, targets in sorted(all_deps.items(), key=lambda x: x[0]):
        print(trigger)
        for target in sorted(targets):
            print(f"    {target}")

