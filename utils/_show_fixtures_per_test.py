from pathlib import Path


def _show_fixtures_per_test(config: Config, session: Session) -> None:
    import _pytest.config

    session.perform_collect()
    invocation_dir = config.invocation_params.dir
    tw = _pytest.config.create_terminal_writer(config)
    verbose = config.get_verbosity()

    def get_best_relpath(func) -> str:
        loc = getlocation(func, invocation_dir)
        return bestrelpath(invocation_dir, Path(loc))

    def write_fixture(fixture_def: FixtureDef[object]) -> None:
        argname = fixture_def.argname
        if verbose <= 0 and argname.startswith("_"):
            return
        prettypath = _pretty_fixture_path(invocation_dir, fixture_def.func)
        tw.write(f"{argname}", green=True)
        tw.write(f" -- {prettypath}", yellow=True)
        tw.write("\n")
        fixture_doc = inspect.getdoc(fixture_def.func)
        if fixture_doc:
            write_docstring(
                tw,
                fixture_doc.split("\n\n", maxsplit=1)[0]
                if verbose <= 0
                else fixture_doc,
            )
        else:
            tw.line("    no docstring available", red=True)

    def write_item(item: nodes.Item) -> None:
        fixturedefs = list(_get_fixtures_per_test(item))
        if not fixturedefs:
            # This test item does not use any fixtures.
            return

        tw.line()
        tw.sep("-", f"fixtures used by {item.name}")
        # TODO: Fix this type ignore.
        tw.sep("-", f"({get_best_relpath(item.function)})")  # type: ignore[attr-defined]

        for fixturedef in fixturedefs:
            write_fixture(fixturedef)

    for session_item in session.items:
        write_item(session_item)

