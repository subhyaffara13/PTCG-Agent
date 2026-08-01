
def _fast_poke_clone(p: dict) -> dict:
    c = {}
    for k, v in p.items():
        if k == "attached" and isinstance(v, list):
            c[k] = list(v)
        elif isinstance(v, dict):
            c[k] = _fast_poke_clone(v)
        else:
            c[k] = v
    return c


def _fast_poke_clone(p: dict) -> dict:
    c = {}
    for k, v in p.items():
        if k == "attached" and isinstance(v, list):
            c[k] = list(v)
        elif isinstance(v, dict):
            c[k] = _fast_poke_clone(v)
        else:
            c[k] = v
    return c

