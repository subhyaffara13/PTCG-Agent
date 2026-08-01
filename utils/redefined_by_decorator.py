
def redefined_by_decorator(node: nodes.FunctionDef) -> bool:
    """Return True if the object is a method redefined via decorator.

    For example:
        @property
        def x(self): return self._x
        @x.setter
        def x(self, value): self._x = value
    """
    if node.decorators:
        for decorator in node.decorators.nodes:
            if (
                isinstance(decorator, nodes.Attribute)
                and getattr(decorator.expr, "name", None) == node.name
            ):
                return True
    return False

