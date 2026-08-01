
def _format_fx_node(n: Node) -> str:
    """
    Format a torch.fx.Node into a human-readable string for debug logging.

    Args:
        n (torch.fx.Node): The FX node being executed.

    Returns:
        str: A formatted string describing the node operation, including its
        name, target, positional arguments, and keyword arguments.
    """
    module_prefix = getattr(n.target, "__module__", "")
    module_prefix = f"{module_prefix}." if module_prefix else ""

    # Handle positional and keyword arguments
    args = ", ".join(map(str, n.args))
    kwargs = ", ".join(f"{k}={v}" for k, v in n.kwargs.items())
    joined = ", ".join(filter(None, [args, kwargs]))

    return (
        f"{n.name} = {module_prefix}{getattr(n.target, '__name__', n.target)}({joined})"
    )

