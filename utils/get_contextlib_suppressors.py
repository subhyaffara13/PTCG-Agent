
def get_contextlib_suppressors(
    node: nodes.NodeNG, exception: type[Exception] | str = Exception
) -> Iterator[nodes.With]:
    """Return the contextlib suppressors handling the exception.

    Args:
        node (nodes.NodeNG): A node that is potentially wrapped in a contextlib.suppress.
        exception (builtin.Exception): exception or name of the exception.

    Yields:
        nodes.With: A with node that is suppressing the exception.
    """
    for with_node in get_contextlib_with_statements(node):
        for item, _ in with_node.items:
            if isinstance(item, nodes.Call):
                inferred = safe_infer(item.func)
                if (
                    isinstance(inferred, nodes.ClassDef)
                    and inferred.qname() == "contextlib.suppress"
                ):
                    if _suppresses_exception(item, exception):
                        yield with_node

