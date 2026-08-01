
def _register_require_version(node):
    # Load the gi.require_version locally
    try:
        import gi

        gi.require_version(node.args[0].value, node.args[1].value)
    except Exception:  # pylint:disable=broad-except
        pass

    return node

