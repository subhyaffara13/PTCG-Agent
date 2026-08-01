
def _module_symbol_table(runtime: types.ModuleType) -> symtable.SymbolTable | None:
    """Retrieve the symbol table for the module (or None on failure).

    1) Use inspect to retrieve the source code of the module
    2) Use symtable to parse the source (and use what symtable knows for its purposes)
    """
    try:
        source = inspect.getsource(runtime)
    except (OSError, TypeError, SyntaxError):
        return None

    try:
        return symtable.symtable(source, runtime.__name__, "exec")
    except SyntaxError:
        return None

