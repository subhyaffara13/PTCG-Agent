
def _auto_declare_smtlib(sym: typing.Union[Symbol, Function], p: SMTLibPrinter, log_warn: typing.Callable[[str], None]):
    if sym.is_Symbol:
        type_signature = p.symbol_table[sym]
        assert isinstance(type_signature, type)
        type_signature = p._known_types[type_signature]
        return p._s_expr('declare-const', [sym, type_signature])

    elif sym.is_Function:
        type_signature = p.symbol_table[type(sym)]
        assert callable(type_signature)
        type_signature = [p._known_types[_] for _ in type_signature.__args__]
        assert len(type_signature) > 0
        params_signature = f"({' '.join(type_signature[:-1])})"
        return_signature = type_signature[-1]
        return p._s_expr('declare-fun', [type(sym), params_signature, return_signature])

    else:
        log_warn(f"Non-Symbol/Function `{sym}` will not be declared.")
        return None

