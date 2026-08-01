
def linerange(node):
    """Get line number range from a node."""
    if hasattr(node, "lineno"):
        return list(range(node.lineno, node.end_lineno + 1))
    else:
        if hasattr(node, "_bandit_linerange_stripped"):
            lines_minmax = node._bandit_linerange_stripped
            return list(range(lines_minmax[0], lines_minmax[1] + 1))

        strip = {
            "body": None,
            "orelse": None,
            "handlers": None,
            "finalbody": None,
        }
        for key in strip.keys():
            if hasattr(node, key):
                strip[key] = getattr(node, key)
                setattr(node, key, [])

        lines_min = 9999999999
        lines_max = -1
        if hasattr(node, "lineno"):
            lines_min = node.lineno
            lines_max = node.lineno
        for n in ast.iter_child_nodes(node):
            lines_minmax = calc_linerange(n)
            lines_min = min(lines_min, lines_minmax[0])
            lines_max = max(lines_max, lines_minmax[1])

        for key in strip.keys():
            if strip[key] is not None:
                setattr(node, key, strip[key])

        if lines_max == -1:
            lines_min = 0
            lines_max = 1

        node._bandit_linerange_stripped = (lines_min, lines_max)

        lines = list(range(lines_min, lines_max + 1))

        """Try and work around a known Python bug with multi-line strings."""
        # deal with multiline strings lineno behavior (Python issue #16806)
        if hasattr(node, "_bandit_sibling") and hasattr(
            node._bandit_sibling, "lineno"
        ):
            start = min(lines)
            delta = node._bandit_sibling.lineno - start
            if delta > 1:
                return list(range(start, node._bandit_sibling.lineno))
        return lines

