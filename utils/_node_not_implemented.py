
def _node_not_implemented(node_name: str) -> Callable[..., None]:
    """
    Return a function that raises a NotImplementedError with a passed node name.
    """

    def f(self, *args, **kwargs):
        raise NotImplementedError(f"'{node_name}' nodes are not implemented")

    return f

