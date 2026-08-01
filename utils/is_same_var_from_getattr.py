
def is_same_var_from_getattr(n1: SymbolNode | None, n2: SymbolNode | None) -> bool:
    """Do n1 and n2 refer to the same Var derived from module-level __getattr__?"""
    return (
        isinstance(n1, Var)
        and n1.from_module_getattr
        and isinstance(n2, Var)
        and n2.from_module_getattr
        and n1.fullname == n2.fullname
    )

