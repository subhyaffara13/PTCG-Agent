
def _get_direct_parametrize_args(node: nodes.Node) -> set[str]:
    """Return all direct parametrization arguments of a node, so we don't
    mistake them for fixtures.

    Check https://github.com/pytest-dev/pytest/issues/5036.

    These things are done later as well when dealing with parametrization
    so this could be improved.
    """
    parametrize_argnames: set[str] = set()
    for marker in node.iter_markers(name="parametrize"):
        indirect = marker.kwargs.get("indirect", False)
        p_argnames, _ = ParameterSet._parse_parametrize_args(
            *marker.args, **marker.kwargs
        )
        p_directness = _resolve_args_directness(p_argnames, indirect, node.nodeid)
        parametrize_argnames.update(
            argname
            for argname, directness in p_directness.items()
            if directness == "direct"
        )
    return parametrize_argnames

