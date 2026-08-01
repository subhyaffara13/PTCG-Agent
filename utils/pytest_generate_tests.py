
def pytest_generate_tests(metafunc):  # type: ignore[no-untyped-def]
    if "loop_factory" not in metafunc.fixturenames:
        return

    loops = metafunc.config.option.aiohttp_loop
    avail_factories: dict[str, Callable[[], asyncio.AbstractEventLoop]]
    avail_factories = {"pyloop": asyncio.new_event_loop}

    if uvloop is not None:  # pragma: no cover
        avail_factories["uvloop"] = uvloop.new_event_loop

    if loops == "all":
        loops = "pyloop,uvloop?"

    factories = {}  # type: ignore[var-annotated]
    for name in loops.split(","):
        required = not name.endswith("?")
        name = name.strip(" ?")
        if name not in avail_factories:  # pragma: no cover
            if required:
                raise ValueError(
                    "Unknown loop '%s', available loops: %s"
                    % (name, list(factories.keys()))
                )
            else:
                continue
        factories[name] = avail_factories[name]
    metafunc.parametrize(
        "loop_factory", list(factories.values()), ids=list(factories.keys())
    )


def pytest_generate_tests(metafunc: Metafunc) -> None:
    """Generate (multiple) parametrized calls to a test function.

    :param metafunc:
        The :class:`~pytest.Metafunc` helper for the test function.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given function definition,
    only conftest files in the functions's directory and its parent directories
    are consulted.
    """


def pytest_generate_tests(metafunc: Metafunc) -> None:
    for marker in metafunc.definition.iter_markers(name="parametrize"):
        metafunc.parametrize(*marker.args, **marker.kwargs, _param_mark=marker)

