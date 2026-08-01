
def is_method_call(
    func: bases.BoundMethod, types: tuple[str, ...] = (), methods: tuple[str, ...] = ()
) -> bool:
    """Determines if a BoundMethod node represents a method call.

    Args:
      func: The BoundMethod AST node to check.
      types: Optional sequence of caller type names to restrict check.
      methods: Optional sequence of method names to restrict check.

    Returns:
      true if the node represents a method call for the given type and
      method names, False otherwise.
    """
    return (
        isinstance(func, astroid.BoundMethod)
        and isinstance(func.bound, astroid.Instance)
        and (func.bound.name in types if types else True)
        and (func.name in methods if methods else True)
    )

