
def _set_module(typevarlike):
    # for pickling:
    def_mod = _caller(depth=2)
    if def_mod != 'typing_extensions':
        typevarlike.__module__ = def_mod


def _set_module(model, submodule_key, module):
    tokens = submodule_key.split(".")
    sub_tokens = tokens[:-1]
    cur_mod = model
    for s in sub_tokens:
        cur_mod = getattr(cur_mod, s)

    setattr(cur_mod, tokens[-1], module)

