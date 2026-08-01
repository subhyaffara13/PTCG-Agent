
def pytest_collection_finish(session: pytest.Session) -> None:
    for i, item in reversed(list(enumerate(session.items))):
        if (
            isinstance(item, pytest.Function)
            and iscoroutinefunction(item.function)
            and item.get_closest_marker("anyio") is not None
            and "anyio_backend" not in item.fixturenames
        ):
            new_items = []
            try:
                cs_fields = {f.name for f in dataclasses.fields(CallSpec2)}
            except TypeError:
                cs_fields = set()

            for param_index, backend in enumerate(get_available_backends()):
                if "_arg2scope" in cs_fields:  # pytest >= 8
                    callspec = CallSpec2(
                        params={"anyio_backend": backend},
                        indices={"anyio_backend": param_index},
                        _arg2scope={"anyio_backend": Scope.Module},
                        _idlist=[backend],
                        marks=[],
                    )
                else:  # pytest 7.x
                    callspec = CallSpec2(  # type: ignore[call-arg]
                        funcargs={},
                        params={"anyio_backend": backend},
                        indices={"anyio_backend": param_index},
                        arg2scope={"anyio_backend": Scope.Module},
                        idlist=[backend],
                        marks=[],
                    )

                fi = item._fixtureinfo
                new_names_closure = list(fi.names_closure)
                if "anyio_backend" not in new_names_closure:
                    new_names_closure.append("anyio_backend")

                new_fixtureinfo = FuncFixtureInfo(
                    argnames=fi.argnames,
                    initialnames=fi.initialnames,
                    names_closure=new_names_closure,
                    name2fixturedefs=fi.name2fixturedefs,
                )
                new_item = pytest.Function.from_parent(
                    item.parent,
                    name=f"{item.originalname}[{backend}]",
                    callspec=callspec,
                    callobj=item.obj,
                    fixtureinfo=new_fixtureinfo,
                    keywords=item.keywords,
                    originalname=item.originalname,
                )
                new_items.append(new_item)

            session.items[i : i + 1] = new_items


def pytest_collection_finish(session: Session) -> None:
    """Called after collection has been performed and modified.

    :param session: The pytest session object.

    Use in conftest plugins
    =======================

    Any conftest plugin can implement this hook.
    """

