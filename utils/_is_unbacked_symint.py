
def _is_unbacked_symint(symbol):
    if not isinstance(symbol, torch.SymInt):
        return False

    return symbol.node.shape_env.is_unbacked_symint(symbol.node.expr)

