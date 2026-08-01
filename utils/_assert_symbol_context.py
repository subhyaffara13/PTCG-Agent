
def _assert_symbol_context(symbolic_context: object) -> TypeGuard[SymbolicContext]:
    if not isinstance(symbolic_context, SymbolicContext):
        raise AssertionError("Invalid symbolic_context object")
    if type(symbolic_context) is SymbolicContext:
        raise AssertionError("Illegal usage of symbolic_context ABC")
    return True

