
def _format_target(base: str, target: str) -> str:
    elems = target.split(".")
    r = base
    for e in elems:
        if not e.isidentifier():
            r = f'getattr({r}, "{e}")'
        else:
            r = f"{r}.{e}"
    return r

