
def parse_tag(tag: str, *, validate_order: bool = False) -> frozenset[Tag]:
    """
    Parses the provided tag (e.g. `py3-none-any`) into a frozenset of
    :class:`Tag` instances.

    Returning a set is required due to the possibility that the tag is a
    `compressed tag set`_, e.g. ``"py2.py3-none-any"`` which supports both
    Python 2 and Python 3.

    If **validate_order** is true, compressed tag set components are checked
    to be in sorted order as required by PEP 425.

    :param str tag: The tag to parse, e.g. ``"py3-none-any"``.
    :param bool validate_order: Check whether compressed tag set components
        are in sorted order.
    :raises UnsortedTagsError: If **validate_order** is true and any compressed tag
        set component is not in sorted order.

    .. versionadded:: 26.1
       The *validate_order* parameter.
    """
    tags = set()
    interpreters, abis, platforms = tag.split("-")
    if validate_order:
        for component in (interpreters, abis, platforms):
            parts = component.split(".")
            if parts != sorted(parts):
                raise UnsortedTagsError(
                    f"Tag component {component!r} is not in sorted order per PEP 425"
                )
    for interpreter in interpreters.split("."):
        for abi in abis.split("."):
            for platform_ in platforms.split("."):
                tags.add(Tag(interpreter, abi, platform_))
    return frozenset(tags)


def parse_tag(tag: str) -> frozenset[Tag]:
    """
    Parses the provided tag (e.g. `py3-none-any`) into a frozenset of Tag instances.

    Returning a set is required due to the possibility that the tag is a
    compressed tag set.
    """
    tags = set()
    interpreters, abis, platforms = tag.split("-")
    for interpreter in interpreters.split("."):
        for abi in abis.split("."):
            for platform_ in platforms.split("."):
                tags.add(Tag(interpreter, abi, platform_))
    return frozenset(tags)


def parse_tag(tag: str) -> FrozenSet[Tag]:
    """
    Parses the provided tag (e.g. `py3-none-any`) into a frozenset of Tag instances.

    Returning a set is required due to the possibility that the tag is a
    compressed tag set.
    """
    tags = set()
    interpreters, abis, platforms = tag.split("-")
    for interpreter in interpreters.split("."):
        for abi in abis.split("."):
            for platform_ in platforms.split("."):
                tags.add(Tag(interpreter, abi, platform_))
    return frozenset(tags)


def parse_tag(tag: str, *, validate_order: bool = False) -> frozenset[Tag]:
    """
    Parses the provided tag (e.g. `py3-none-any`) into a frozenset of
    :class:`Tag` instances.

    Returning a set is required due to the possibility that the tag is a
    `compressed tag set`_, e.g. ``"py2.py3-none-any"`` which supports both
    Python 2 and Python 3.

    If **validate_order** is true, compressed tag set components are checked
    to be in sorted order as required by PEP 425.

    :param str tag: The tag to parse, e.g. ``"py3-none-any"``.
    :param bool validate_order: Check whether compressed tag set components
        are in sorted order.
    :raises UnsortedTagsError: If **validate_order** is true and any compressed tag
        set component is not in sorted order.

    .. versionadded:: 26.1
       The *validate_order* parameter.
    """
    tags = set()
    interpreters, abis, platforms = tag.split("-")
    if validate_order:
        for component in (interpreters, abis, platforms):
            parts = component.split(".")
            if parts != sorted(parts):
                raise UnsortedTagsError(
                    f"Tag component {component!r} is not in sorted order per PEP 425"
                )
    for interpreter in interpreters.split("."):
        for abi in abis.split("."):
            for platform_ in platforms.split("."):
                tags.add(Tag(interpreter, abi, platform_))
    return frozenset(tags)

