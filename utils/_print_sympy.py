
def _print_sympy(s: torch.SymInt | torch.SymBool | torch.SymFloat | sympy.Expr):
    if isinstance(s, (torch.SymInt, torch.SymBool, torch.SymFloat)):
        s = s.node.expr
    return sympy.printing.repr.srepr(s)

