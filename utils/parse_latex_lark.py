
def parse_latex_lark(s: str):
    """
    Experimental LaTeX parser using Lark.

    This function is still under development and its API may change with the
    next releases of SymPy.
    """
    if _lark is None:
        raise ImportError("Lark is probably not installed")
    return _lark_latex_parser.doparse(s)

