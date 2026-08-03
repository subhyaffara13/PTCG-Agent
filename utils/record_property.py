from typing import Callable

def record_property(request: FixtureRequest) -> Callable[[str, object], None]:
    """Add extra properties to the calling test.

    User properties become part of the test report and are available to the
    configured reporters, like JUnit XML.

    The fixture is callable with ``name, value``. The value is automatically
    XML-encoded.

    Example::

        def test_function(record_property):
            record_property("example_key", 1)
    """
    _warn_incompatibility_with_xunit2(request, "record_property")

    def append_property(name: str, value: object) -> None:
        request.node.user_properties.append((name, value))

    return append_property

