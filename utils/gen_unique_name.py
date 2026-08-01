
def gen_unique_name(base: str, table: SymbolTable) -> str:
    """Generate a name that does not appear in table by appending numbers to base."""
    if base not in table:
        return base
    i = 1
    while base + str(i) in table:
        i += 1
    return base + str(i)

