from typing import Any

def pytest_fixture_post_finalizer(
    fixturedef: FixtureDef[Any], request: SubRequest
) -> None:
    """Called after fixture teardown, but before the cache is cleared, so
    the fixture result ``fixturedef.cached_result`` is still available (not
    ``None``).

    :param fixturedef:
        The fixture definition object.
    :param request:
        The fixture request object.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given fixture, only
    conftest files in the fixture scope's directory and its parent directories
    are consulted.
    """


def pytest_fixture_post_finalizer(
    fixturedef: FixtureDef[object], request: SubRequest
) -> None:
    if fixturedef.cached_result is not None:
        config = request.config
        if config.option.setupshow:
            _show_fixture_action(fixturedef, request.config, "TEARDOWN")
            if hasattr(fixturedef, "cached_param"):
                del fixturedef.cached_param

