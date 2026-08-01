
def is_complex_format_str(node: nodes.NodeNG) -> bool:
    """Return whether the node represents a string with complex formatting specs."""
    inferred = utils.safe_infer(node)
    if not (isinstance(inferred, nodes.Const) and isinstance(inferred.value, str)):
        return True
    try:
        parsed = list(string.Formatter().parse(inferred.value))
    except ValueError:
        # This format string is invalid
        return False
    return any(format_spec for (_, _, format_spec, _) in parsed)

