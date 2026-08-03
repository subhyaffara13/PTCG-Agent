from typing import Any, Callable

def register_fixture(
    *,
    name: str,
    func: _FixtureFunc[object],
    node: nodes.Node,
    scope: ScopeName | Callable[[str, Config], ScopeName] = "function",
    params: Sequence[object] | None = None,
    ids: tuple[object | None, ...] | Callable[[Any], object | None] | None = None,
    autouse: bool = False,
) -> None:
    """Register a fixture imperatively.

    This is an advanced function intended for use by plugins.

    Normally, fixtures should be registered declaratively using the
    :func:`@pytest.fixture <pytest.fixture>` decorator. Pytest looks for these
    fixture definitions during the collection phase and registers them
    automatically. For some plugin usecases the declarative interface can be
    cumbersome or nonviable, in which case the imperative interface can be used.

    Fixture registration is expected to happen during the collection phase, and
    this is the only sanctioned use. However, to allow for more creative uses,
    this is not enforced. But do so at your own risk!

    .. versionadded: 9.1

    :param name:
        The fixture's name.
    :param func:
        The fixture's implementation function.
    :param node:
        The visibility of the fixture.

        Only items that are descendents of this node in the collection tree will
        be able to request this fixture. You can think of this as the place
        where you would put the `@pytest.fixture`.

        For global visibility, pass the :class:`session <pytest.Session>` node,
        which is the root of the collection tree.
    :param scope:
        The fixture's scope.
    :param params:
        The fixture's parametrization params.
    :param ids:
        The fixture's IDs.
    :param autouse:
        Whether this is an autouse fixture.
    """
    node.session._fixturemanager._register_fixture(
        name=name,
        func=func,
        node=node,
        scope=scope,
        params=params,
        ids=ids,
        autouse=autouse,
    )

