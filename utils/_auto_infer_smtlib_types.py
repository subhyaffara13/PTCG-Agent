
def _auto_infer_smtlib_types(
    *exprs: Basic,
    symbol_table: typing.Optional[dict] = None
) -> dict:
    # [TYPE INFERENCE RULES]
    # X is alone in an expr => X is bool
    # X in BooleanFunction.args => X is bool
    # X matches to a bool param of a symbol_table function => X is bool
    # X matches to an int param of a symbol_table function => X is int
    # X.is_integer => X is int
    # X == Y, where X is T => Y is T

    # [FALLBACK RULES]
    # see _auto_declare_smtlib(..)
    # X is not bool and X is not int and X is Symbol => X is float
    # else (e.g. X is Function) => error. must be specified explicitly.

    _symbols = dict(symbol_table) if symbol_table else {}

    def safe_update(syms: set, inf):
        for s in syms:
            assert s.is_Symbol
            if (old_type := _symbols.setdefault(s, inf)) != inf:
                raise TypeError(f"Could not infer type of `{s}`. Apparently both `{old_type}` and `{inf}`?")

    # EXPLICIT TYPES
    safe_update({
        e
        for e in exprs
        if e.is_Symbol
    }, bool)

    safe_update({
        symbol
        for e in exprs
        for boolfunc in e.atoms(BooleanFunction)
        for symbol in boolfunc.args
        if symbol.is_Symbol
    }, bool)

    safe_update({
        symbol
        for e in exprs
        for boolfunc in e.atoms(Function)
        if type(boolfunc) in _symbols
        for symbol, param in zip(boolfunc.args, _symbols[type(boolfunc)].__args__)
        if symbol.is_Symbol and param == bool
    }, bool)

    safe_update({
        symbol
        for e in exprs
        for intfunc in e.atoms(Function)
        if type(intfunc) in _symbols
        for symbol, param in zip(intfunc.args, _symbols[type(intfunc)].__args__)
        if symbol.is_Symbol and param == int
    }, int)

    safe_update({
        symbol
        for e in exprs
        for symbol in e.atoms(Symbol)
        if symbol.is_integer
    }, int)

    safe_update({
        symbol
        for e in exprs
        for symbol in e.atoms(Symbol)
        if symbol.is_real and not symbol.is_integer
    }, float)

    # EQUALITY RELATION RULE
    rels_eq = [rel for expr in exprs for rel in expr.atoms(Equality)]
    rels = [
               (rel.lhs, rel.rhs) for rel in rels_eq if rel.lhs.is_Symbol
           ] + [
               (rel.rhs, rel.lhs) for rel in rels_eq if rel.rhs.is_Symbol
           ]
    for infer, reltd in rels:
        inference = (
            _symbols[infer] if infer in _symbols else
            _symbols[reltd] if reltd in _symbols else

            _symbols[type(reltd)].__args__[-1]
            if reltd.is_Function and type(reltd) in _symbols else

            bool if reltd.is_Boolean else
            int if reltd.is_integer or reltd.is_Integer else
            float if reltd.is_real else
            None
        )
        if inference: safe_update({infer}, inference)

    return _symbols

