
def pytest_pycollect_makeitem(collector, name, obj):  # type: ignore[no-untyped-def]
    """Fix pytest collecting for coroutines."""
    if collector.funcnamefilter(name) and inspect.iscoroutinefunction(obj):
        return list(collector._genfunctions(name, obj))


def pytest_pycollect_makeitem(
    collector: pytest.Module | pytest.Class, name: str, obj: object
) -> None:
    if collector.istestfunction(obj, name):
        inner_func = obj.hypothesis.inner_test if hasattr(obj, "hypothesis") else obj
        if iscoroutinefunction(inner_func):
            anyio_auto_mode = collector.config.getini("anyio_mode") == "auto"
            marker = collector.get_closest_marker("anyio")
            own_markers = getattr(obj, "pytestmark", ())
            if (
                anyio_auto_mode
                or marker
                or any(marker.name == "anyio" for marker in own_markers)
            ):
                pytest.mark.usefixtures("anyio_backend")(obj)


def pytest_pycollect_makeitem(
    collector: Module | Class, name: str, obj: object
) -> None | Item | Collector | list[Item | Collector]:
    """Return a custom item/collector for a Python object in a module, or None.

    Stops at first non-None result, see :ref:`firstresult`.

    :param collector:
        The module/class collector.
    :param name:
        The name of the object in the module/class.
    :param obj:
        The object.
    :returns:
        The created items/collectors.

    Use in conftest plugins
    =======================

    Any conftest file can implement this hook. For a given collector, only
    conftest files in the collector's directory and its parent directories
    are consulted.
    """


def pytest_pycollect_makeitem(
    collector: Module | Class, name: str, obj: object
) -> None | nodes.Item | nodes.Collector | list[nodes.Item | nodes.Collector]:
    assert isinstance(collector, Class | Module), type(collector)
    # Nothing was collected elsewhere, let's do it here.
    if safe_isclass(obj):
        if collector.istestclass(obj, name):
            return Class.from_parent(collector, name=name, obj=obj)
    elif collector.istestfunction(obj, name):
        # mock seems to store unbound methods (issue473), normalize it.
        obj = getattr(obj, "__func__", obj)
        # We need to try and unwrap the function if it's a functools.partial
        # or a functools.wrapped.
        # We mustn't if it's been wrapped with mock.patch (python 2 only).
        if not (inspect.isfunction(obj) or inspect.isfunction(get_real_func(obj))):
            filename, lineno = getfslineno(obj)
            warnings.warn_explicit(
                message=PytestCollectionWarning(
                    f"cannot collect {name!r} because it is not a function."
                ),
                category=None,
                filename=str(filename),
                lineno=lineno + 1,
            )
        elif getattr(obj, "__test__", True):
            if inspect.isgeneratorfunction(obj):
                fail(
                    f"'yield' keyword is allowed in fixtures, but not in tests ({name})",
                    pytrace=False,
                )
            return list(collector._genfunctions(name, obj))
        return None
    return None


def pytest_pycollect_makeitem(
    collector: Module | Class, name: str, obj: object
) -> UnitTestCase | None:
    try:
        # Has unittest been imported?
        ut = sys.modules["unittest"]
        # Is obj a subclass of unittest.TestCase?
        # Type ignored because `ut` is an opaque module.
        if not issubclass(obj, ut.TestCase):  # type: ignore
            return None
    except Exception:
        return None
    # Is obj a concrete class?
    # Abstract classes can't be instantiated so no point collecting them.
    if inspect.isabstract(obj):
        return None
    # Yes, so let's collect it.
    return UnitTestCase.from_parent(collector, name=name, obj=obj)


def pytest_pycollect_makeitem(collector: Any, name: str, obj: object) -> Any | None:
    """Called by pytest on each object in modules configured in conftest.py files.

    collector is pytest.Collector, returns Optional[pytest.Class]
    """
    if isinstance(obj, type):
        # Only classes derived from DataSuite contain test cases, not the DataSuite class itself
        if issubclass(obj, DataSuite) and obj is not DataSuite:
            # Non-None result means this obj is a test case.
            # The collect method of the returned DataSuiteCollector instance will be called later,
            # with self.obj being obj.
            return DataSuiteCollector.from_parent(parent=collector, name=name)
    return None

