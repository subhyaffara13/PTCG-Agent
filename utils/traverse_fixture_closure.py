
def traverse_fixture_closure(
    initialnames: Iterable[str],
    *,
    getfixturedefs: Callable[[str], Sequence[FixtureDef[Any]] | None],
) -> Iterator[str]:
    """Statically traverse the fixture dependency closure in DFS order starting
    from initialnames, yielding all requested fixture names (argnames).

    Each argname is only yielded once.
    """
    # Track the index for each fixture name in the simulated stack.
    # Needed for handling override chains correctly, similar to
    # FixtureRequest._get_active_fixturedef.
    # Using negative indices: -1 is the most specific (last), -2 is second to
    # last, etc.
    current_indices: dict[str, int] = {}

    def process_argname(argname: str) -> Iterator[str]:
        index = current_indices.get(argname)

        # Optimization: already processed this argname.
        if index == -1:
            return

        # Only yield each argname once.
        if index is None:
            yield argname
            current_indices[argname] = -1

        fixturedefs = getfixturedefs(argname)
        if not fixturedefs:
            return

        index = current_indices.get(argname, -1)
        if -index > len(fixturedefs):
            # Exhausted the override chain (will error during runtest).
            return
        fixturedef = fixturedefs[index]

        current_indices[argname] = index - 1
        for dep in fixturedef.argnames:
            yield from process_argname(dep)
        current_indices[argname] = index

    for argname in initialnames:
        yield from process_argname(argname)

