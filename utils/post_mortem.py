
def post_mortem(tb_or_exc: types.TracebackType | BaseException) -> None:
    p = pytestPDB._init_pdb("post_mortem")
    p.reset()
    p.interaction(None, tb_or_exc)
    if p.quitting:
        outcomes.exit("Quitting debugger")

