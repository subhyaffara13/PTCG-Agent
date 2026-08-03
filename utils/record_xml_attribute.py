from typing import Callable

def record_xml_attribute(request: FixtureRequest) -> Callable[[str, object], None]:
    """Add extra xml attributes to the tag for the calling test.

    The fixture is callable with ``name, value``. The value is
    automatically XML-encoded.
    """
    from _pytest.warning_types import PytestExperimentalApiWarning

    request.node.warn(
        PytestExperimentalApiWarning("record_xml_attribute is an experimental feature")
    )

    _warn_incompatibility_with_xunit2(request, "record_xml_attribute")

    # Declare noop
    def add_attr_noop(name: str, value: object) -> None:
        pass

    attr_func = add_attr_noop

    xml = request.config.stash.get(xml_key, None)
    if xml is not None:
        node_reporter = xml.node_reporter(request.node.nodeid)
        attr_func = node_reporter.add_attribute

    return attr_func

