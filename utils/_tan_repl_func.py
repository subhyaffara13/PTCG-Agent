
def _tan_repl_func(expr):
    """Replace tan with sin/cos."""
    if isinstance(expr, tan):
        return sin(*expr.args) / cos(*expr.args)
    elif not expr.args or expr.is_Derivative:
        return expr

