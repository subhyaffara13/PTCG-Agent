
def _contexts_from_module() -> dict[type[ast.expr_context], Context]:
    return {
        ast.Load: Context.Load,
        ast.Store: Context.Store,
        ast.Del: Context.Del,
        ast.Param: Context.Store,
    }

