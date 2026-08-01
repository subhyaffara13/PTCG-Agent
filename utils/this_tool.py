
def this_tool() -> 'Tool':
    """Deprecated — Alias of :func:`cyclonedx.contrib.this.builders.this_tool`.

    .. deprecated:: next
        This re-export location is deprecated.
        Use ``from cyclonedx.contrib.this.builders import this_tool`` instead.
        The exported symbol itself is NOT deprecated — only this import path.
    """
    return _this_tool()


def this_tool() -> Tool:
    """Representation of this very python library as a :class:`cyclonedx.model.tool.Tool`."""
    return Tool.from_component(this_component())

