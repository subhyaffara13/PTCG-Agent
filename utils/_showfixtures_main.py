
def _showfixtures_main(config: Config, session: Session) -> None:
    import _pytest.config

    session.perform_collect()
    invocation_dir = config.invocation_params.dir
    tw = _pytest.config.create_terminal_writer(config)
    verbose = config.get_verbosity()

    fm = session._fixturemanager

    available = []
    seen: set[tuple[str, str]] = set()

    for argname, fixturedefs in fm._arg2fixturedefs.items():
        assert fixturedefs is not None
        if not fixturedefs:
            continue
        for fixturedef in fixturedefs:
            loc = getlocation(fixturedef.func, invocation_dir)
            if (fixturedef.argname, loc) in seen:
                continue
            seen.add((fixturedef.argname, loc))
            available.append(
                (
                    len(fixturedef.baseid),
                    fixturedef.func.__module__,
                    _pretty_fixture_path(invocation_dir, fixturedef.func),
                    fixturedef.argname,
                    fixturedef,
                )
            )

    available.sort()
    currentmodule = None
    for baseid, module, prettypath, argname, fixturedef in available:
        if currentmodule != module:
            if not module.startswith("_pytest."):
                tw.line()
                tw.sep("-", f"fixtures defined from {module}")
                currentmodule = module
        if verbose <= 0 and argname.startswith("_"):
            continue
        tw.write(f"{argname}", green=True)
        if fixturedef.scope != "function":
            tw.write(f" [{fixturedef.scope} scope]", cyan=True)
        tw.write(f" -- {prettypath}", yellow=True)
        tw.write("\n")
        doc = inspect.getdoc(fixturedef.func)
        if doc:
            write_docstring(
                tw, doc.split("\n\n", maxsplit=1)[0] if verbose <= 0 else doc
            )
        else:
            tw.line("    no docstring available", red=True)
        tw.line()

