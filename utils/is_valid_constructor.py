
def is_valid_constructor(n: SymbolNode | None) -> bool:
    """Does this node represents a valid constructor method?

    This includes normal functions, overloaded functions, and decorators
    that return a callable type.
    """
    if isinstance(n, SYMBOL_FUNCBASE_TYPES):
        return True
    if isinstance(n, Decorator):
        return isinstance(get_proper_type(n.type), FunctionLike)
    return False

