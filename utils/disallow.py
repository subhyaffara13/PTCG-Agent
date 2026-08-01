
def disallow(nodes: set[str]) -> Callable[[type[_T]], type[_T]]:
    """
    Decorator to disallow certain nodes from parsing. Raises a
    NotImplementedError instead.

    Returns
    -------
    callable
    """

    def disallowed(cls: type[_T]) -> type[_T]:
        # error: "Type[_T]" has no attribute "unsupported_nodes"
        cls.unsupported_nodes = ()  # type: ignore[attr-defined]
        for node in nodes:
            new_method = _node_not_implemented(node)
            name = f"visit_{node}"
            # error: "Type[_T]" has no attribute "unsupported_nodes"
            cls.unsupported_nodes += (name,)  # type: ignore[attr-defined]
            setattr(cls, name, new_method)
        return cls

    return disallowed

