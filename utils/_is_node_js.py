
def _is_node_js() -> bool:
    """
    Check if we are in Node.js.

    :return: True if we are in Node.js.
    :rtype: bool
    """
    return (
        hasattr(js, "process")
        and hasattr(js.process, "release")
        # According to the Node.js documentation, the release name is always "node".
        and js.process.release.name == "node"
    )


def _is_node_js() -> bool:
    """
    Check if we are in Node.js.

    :return: True if we are in Node.js.
    :rtype: bool
    """
    return (
        hasattr(js, "process")
        and hasattr(js.process, "release")
        # According to the Node.js documentation, the release name is always "node".
        and js.process.release.name == "node"
    )

