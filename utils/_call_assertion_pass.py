
def _call_assertion_pass(lineno: int, orig: str, expl: str) -> None:
    if util._assertion_pass is not None:
        util._assertion_pass(lineno, orig, expl)

