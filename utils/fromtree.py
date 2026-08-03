from typing import Any, Optional

def fromtree(
    tree: etree.Element,
    use_builtin_types: Optional[bool] = None,
    dict_type: Type[MutableMapping[str, Any]] = dict,
) -> Any:
    """Convert an XML tree to a plist structure.

    Args:
        tree: An ``etree`` ``Element``.
        use_builtin_types: If True, binary data is deserialized to
            bytes strings. If False, it is wrapped in :py:class:`Data`
            objects. Defaults to True if not provided. Deprecated.
        dict_type: What type to use for dictionaries.

    Returns: An object (usually a dictionary).
    """
    target = PlistTarget(use_builtin_types=use_builtin_types, dict_type=dict_type)
    for action, element in etree.iterwalk(tree, events=("start", "end")):
        if action == "start":
            target.start(element.tag, element.attrib)
        elif action == "end":
            # if there are no children, parse the leaf's data
            if not len(element):
                # always pass str, not None
                target.data(element.text or "")
            target.end(element.tag)
    return target.close()

